#!/usr/bin/python3

from flask import Flask, jsonify, make_response
import subprocess

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
	return "Hello world!"

#
# This function retrieves information related to host's operating system.
# Command to be used 'uname'
#
@app.route('/os',methods=['GET'])
def os():
	kernel = subprocess.check_output(['uname','-s'])
	release = subprocess.check_output(['uname','-r'])
	nodename = subprocess.check_output(['uname','-n'])
	kernelv = subprocess.check_output(['uname','-v'])
	machine = subprocess.check_output(['uname','-m'])
	processor = subprocess.check_output(['uname','-p'])
	os = subprocess.check_output(['uname','-o'])
	hardware = subprocess.check_output(['uname','-i'])
	return jsonify({'kernel': kernel,
			'release': release,
			'node_name': nodename,
			'kernel_version': kernelv,
			'machine': machine,
			'processor': processor,
			'operating_system': os,
			'hardware_platform': hardware})

#
# This function retrieves information related to a specific parameter
# of a host. Commando to be used 'uname'
#
# Possible values:
#
# - kernel
# - release
# - nodename
# - kernelversion
# - machine
# - processor
# - operatingsystem
# - hardware
#
@app.route('/os/<string:param>',methods=['GET'])
def osp(param):
	key = param
	value = ""
	if (param == "kernel"):
		value = subprocess.check_output(['uname','-s'])
	elif (param == "release"):
		value = subprocess.check_output(['uname','-r'])
	elif (param == "nodename"):
		value = subprocess.check_output(['uname','-n'])
	elif (param == "kernelversion"):
		value = subprocess.check_output(['uname','-v'])
	elif (param == "machine"):
		value = subprocess.check_output(['uname','-m'])
	elif (param == "processor"):
		value = subprocess.check_output(['uname','-p'])
	elif (param == "operatingsystem"):
		value = subprocess.check_output(['uname','-o'])
	elif (param == "hardware"):
		value = subprocess.check_output(['uname','-i'])
	else:
		return make_response(jsonify({'error': 'Bad parameter. Valid parameters: \'kernel\', \'release\' \'nodename\' \'kernelversion\' \'machine\' \'processor\' \'operatingsystem\' \'hardware\''}), 404)

	return jsonify({key: value})

#
# Method used to determine who is logged in. Command to be used 'who'
#
@app.route('/who',methods = ['GET'])
def who():
	who = subprocess.Popen(['who'], stdout = subprocess.PIPE)
	cut = subprocess.Popen(['cut', '-d', ' ', '-f', '1'], stdin = who.stdout, stdout = subprocess.PIPE)
	output = subprocess.check_output(('uniq'), stdin = cut.stdout)
	return jsonify({'users': output})

#
# Method used to determine if a particular user is logged in. Command to be used
# 'who'
#
@app.route('/who/<string:user>',methods = ['GET'])
def whou(user):
	who = subprocess.Popen(['who'], stdout = subprocess.PIPE)
	cut = subprocess.Popen(['cut', '-d', ' ', '-f', '1'], stdin = who.stdout, stdout = subprocess.PIPE)
	grep = subprocess.Popen(['grep', user], stdin = cut.stdout, stdout = subprocess.PIPE)
	output = subprocess.check_output(('uniq'), stdin = grep.stdout)
	return jsonify({'loggedin': output})

#
# Method used to determine CPU usage. Command to be used 'vmstat'
#
@app.route('/cpu/<string:param>', methods = ['GET'])
def cpuwa(param):
	vmstat = subprocess.Popen(['vmstat'], stdout = subprocess.PIPE)
	tail = subprocess.Popen(['tail','-n','+3'], stdin = vmstat.stdout, stdout = subprocess.PIPE)
	tr = subprocess.Popen(['tr', '-s', ' '], stdin = tail.stdout, stdout = subprocess.PIPE)
	if (param == "us"):
		value = "14"
	elif (param == "sy"):
		value = "15"
	elif (param == "id"):
		value = "16"
	elif (param == "wa"):
		value = "17"
	elif (param == "st"):
		value = "18"
	else:
		return make_response(jsonify({'error': 'Possible values us, sy, id, wa, st'}), 404)

	output = subprocess.check_output(['cut', '-d', ' ', '-f', value], stdin = tr.stdout)
	return jsonify({'cpu %s' % param: output})

#
# Method used to determine MEMORY usage. Command to be used 'vmstat'
#
@app.route('/mem/<string:param>', methods = ['GET'])
def mem(param):
	vmstat = subprocess.Popen(['vmstat'], stdout = subprocess.PIPE)
	tail = subprocess.Popen(['tail','-n','+3'], stdin = vmstat.stdout, stdout = subprocess.PIPE)
	tr = subprocess.Popen(['tr', '-s', ' '], stdin = tail.stdout, stdout = subprocess.PIPE)
	if (param == "swpd"):
		value = "4"
	elif (param == "free"):
		value = "5"
	elif (param == "buff"):
		value = "6"
	elif (param == "cache"):
		value = "7"
	else:
		return make_response(jsonify({'error': 'Possible values swpd, free, buff, cache'}), 404)

	output = subprocess.check_output(['cut', '-d', ' ', '-f', value], stdin = tr.stdout)
	return jsonify({'mem %s' % param: output})

#
# Method used to determine SWAP behaviour. Command to be used 'vmstat'
#
@app.route('/swap/<string:param>', methods = ['GET'])
def swap(param):
	vmstat = subprocess.Popen(['vmstat'], stdout = subprocess.PIPE)
	tail = subprocess.Popen(['tail','-n','+3'], stdin = vmstat.stdout, stdout = subprocess.PIPE)
	tr = subprocess.Popen(['tr', '-s', ' '], stdin = tail.stdout, stdout = subprocess.PIPE)
	if (param == "si"):
		value = "8"
	elif (param == "so"):
		value = "9"
	else:
		return make_response(jsonify({'error': 'Possible values si, so'}), 404)

	output = subprocess.check_output(['cut', '-d', ' ', '-f', value], stdin = tr.stdout)
	return jsonify({'swap %s' % param: output})
#
# Method used to determine the free disk space on the main partition. comand to be used 'df'
#
@app.route('/disk', methods = ['GET'])
def diskf ():
	dfs = subprocess.Popen(['df', '/'], stdout = subprocess.PIPE)
	tails = subprocess.Popen(['tail', '-n', '1'], stdin = dfs.stdout, stdout = subprocess.PIPE)
	trs = subprocess.Popen(['tr', '-s', ' '], stdin = tails.stdout, stdout = subprocess.PIPE)
	size = str(int(float(subprocess.check_output(['cut', '-d', ' ', '-f', '2'], stdin = trs.stdout))/1048576))

	dff = subprocess.Popen(['df', '/'], stdout = subprocess.PIPE)
	tailf = subprocess.Popen(['tail', '-n', '1'], stdin = dff.stdout, stdout = subprocess.PIPE)
	trf = subprocess.Popen(['tr', '-s', ' '], stdin = tailf.stdout, stdout = subprocess.PIPE)
	free = str(int(float(subprocess.check_output(['cut', '-d', ' ', '-f', '4'], stdin = trf.stdout))/1048576))

	return jsonify({'Disk Size': size, 'Free Disk Space': free})
#
# Method used to determine the free disk space in a determined partition. comand to be used 'df'
#
@app.route('/disk/<string:param>', methods = ['GET'])
def disk (param):
	if (param == "root"):
		value = "/"
	else:
		value = param
	dfs = subprocess.Popen(['df', value], stdout = subprocess.PIPE)
	tails = subprocess.Popen(['tail', '-n', '1'], stdin = dfs.stdout, stdout = subprocess.PIPE)
	trs = subprocess.Popen(['tr', '-s', ' '], stdin = tails.stdout, stdout = subprocess.PIPE)
	size = int(float(subprocess.check_output(['cut', '-d', ' ', '-f', '2'], stdin = trs.stdout))/1048576)

	dff = subprocess.Popen(['df', value], stdout = subprocess.PIPE)
	tailf = subprocess.Popen(['tail', '-n', '1'], stdin = dff.stdout, stdout = subprocess.PIPE)
	trf = subprocess.Popen(['tr', '-s', ' '], stdin = tailf.stdout, stdout = subprocess.PIPE)
	free = int(float(subprocess.check_output(['cut', '-d', ' ', '-f', '4'], stdin = trf.stdout))/1048576)

	return jsonify({'Disk Size ': size, 'Free Disk Space': free})


if __name__ == '__main__':
	app.run(debug = True, host='0.0.0.0', use_reloader=True )
