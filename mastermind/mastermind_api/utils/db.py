import os
import sys
import configparser
import pymysql

config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(os.path.abspath(__file__)), "conf.ini"))

HOST_ADDR = config['database_details']['host_addr']
HOST_PORT = config['database_details']['host_port']
USER = config['database_details']['user']
PASSWORD = config['database_details']['password']
DATABASE_NAME = config['database_details']['database_name']


class DbConnection(object):
	"""docstring for DbConnection"""
	def __init__(self):
		self.config = {
						'host': HOST_ADDR,		
						'database': DATABASE_NAME,
						'user': USER,
						'password': PASSWORD
						}

	def __get_param_select_stmt(self, str_query, params):
		stmt = ""
		out_params = []
		i = 0
		while i < len(params):
			out_params.append("@_"+str(str_query)+"_"+str(i))
			i += 1
		stmt = "SELECT "+str(",".join(out_params))

		return stmt		

	def execute_statement(self, proc_name="", commit = False, params = []):
		res_obj = None
		all_params = []

		try:
			final_result = []
			connection = pymysql.connect(**self.config)

			with connection.cursor(pymysql.cursors.DictCursor) as cursor:
				
				if len(params):
					select_stmt = self.__get_param_select_stmt(proc_name, params)
					cursor.callproc(proc_name, params)
				else:
					cursor.callproc(proc_name)

				while True:

					if cursor.rowcount:
						final_result.append(cursor.fetchall())

					if not cursor.nextset():
						break

				if len(params):		
					cursor.execute(select_stmt)	
					params = cursor.fetchall()[0]
					
					for i in range(0,len(params)):
						key = "@_"+str(proc_name)+"_"+str(i)

						if key in params:
							all_params.append(params[key])
					
				res_obj = Response(True, "", final_result, all_params)

				if commit:
					connection.commit()

		except Exception as e:
			res_obj = Response(False, e, None, all_params)
		finally:
			connection.close()

		return res_obj

class Response(object):
	"""docstring for Response"""
	def __init__(self,Status, ErrorMessage, Data, Params):
		self.Status = Status
		self.ErrorMessage = ErrorMessage
		self.Data = Data
		self.Params = Params

	def get_Status(self):
		return self.Status
	
	def get_ErrorMessage(self):
		return self.ErrorMessage
	
	def get_Data(self):
		return self.Data
	
	def get_Params(self):
		return self.Params		


