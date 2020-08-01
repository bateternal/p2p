
class View:
	__APIs = {  
			"GET"	:{},
			"POST"	:{}
			}

	@staticmethod
	def get(url, func):
		View.__APIs['GET'][url] = func

	@staticmethod
	def post(url, func):
		View.__APIs['POST'][url] = func

	@staticmethod
	def call_api(method ,url ,request):
		return View.__APIs[method][url](request)

