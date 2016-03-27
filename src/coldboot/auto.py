import os
import subprocess
import time
import sys
import getopt


def myPrint(msg):
	if g_verbose:
		print(msg)

def execCmdPrint(msg):
	myPrint(msg)

def execCmd(cmd, shell=True):
	myPrint(">>>> %s"%cmd)

	proc = subprocess.Popen(cmd, shell=shell, universal_newlines=True,
							 stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	output = ''.join(proc.stdout.readlines())
	exitcode = proc.wait()
	if exitcode is None:
		exitcode = 0
	myPrint(output)
	# if len(output) > 0:
		# lines = output.split("\n")
		# for line in lines:
			# if len(line) > 0:
				# myPrint(">>>>" + line)
	return (exitcode, output)

def StrCombine(Str1, Str2):
	return "%s %s" % (Str1, Str2)

def adb(cmd):
	return execCmd(StrCombine("adb", cmd))

def adbShell(cmd):
	return adb(StrCombine("shell", cmd))

def adbShellGetProp(params):
	return adbShell(StrCombine("getprop", params))

def adbShellAm(params):
	return adbShell(StrCombine("am", params))

def adbShellAmStart(params):
	return adbShellAm(StrCombine("start -n", params))

def adbShellAmStartApp(package, acitivity):
	conponent = "%s/%s"%(package, acitivity)
	return adbShellAmStart(conponent)

def adbShellGetPropModel():
	return adbShellGetProp("ro.product.model")

def adbShellGetVersionSDK():
	return adbShellGetProp("ro.build.version.sdk")

def adbShellAmStartTargetApp():
	return adbShellAmStartApp(g_package, g_activity)

def adbShellAmForceStop(params):
	return adbShellAm(StrCombine("force-stop", params))

def adbShellAmForceStopTargetApp():
	return adbShellAmForceStop(g_package)

def adbPull(srcFile, dstFile):
	''' not support path contain blank space'''
	cmd1 = "pull %s %s"%(srcFile, dstFile)
	return adb(cmd1)

def adbUninstall(params):
	cmd1 = "uninstall %s"%params
	return adb(cmd1)

def adbInstall(params):
	cmd1 = "install %s"%params
	return adb(cmd1)

def adbInstallR(params):
	cmd1 = "install -r %s"%params
	return adb(cmd1)

def adbInstallApk():
	adbInstall(g_install_apk)

def adbInstallRApk():
	adbInstallR(g_install_apk)

def adbStartServer():
	return adb("start-server")

def adbKillServer():
	return adb("kill-server")

def doTest():
	adbShellGetProp(" ")
	# adbShellGetPropModel()
	# adbShellGetVersionSDK()
	for i in range(0, g_test_count):
		myPrint("--------LOOP TEST %d--------" % (i+1))
		adbShellAmStartTargetApp()
		time.sleep(10)
		adbShellAmForceStopTargetApp()
		time.sleep(5)

def usage():
	print \
'''xxx.py -p com.android.email -a com.android.email.MainActivity -i ~/1.apk
or
xxx.py --package=com.android.email --activity=com.android.email.MainActivity --install-pak=~/1.apk
	-p, --package 			: packageName
	-a, --acitivity			: acitivityName
	-i, --install-apk 		: apk path
	-t, --test-count		: testcount
	-h, --help				: print useage
	-v 						: verbose
'''

g_package = None
g_activity = None
g_install_apk = None
g_verbose = False
g_test_count = 0

def intOpt():
	try:
		opts, args = getopt.getopt(sys.argv[1:], "hvp:a:i:t:",
		 ["help", "verbose", "package=", "activity=", "install-apk=", "test-count="])
	except getopt.GetoptError as error:
		print str(error)
		usage()
		sys.exit(2)
	global g_verbose
	global g_activity
	global g_install_apk
	global g_package
	global g_test_count
	for o, a in opts:
		if o in ("-v", "--verbose"):
			g_verbose = True
		elif o in ("-h", "--help"):
			usage()
			sys.exit()
		elif o in ("-p", "--package"):
			g_package = a
		elif o in ("-a", "--activity"):
			g_activity = a
		elif o in ("-i", "--install-apk"):
			g_install_apk = a
		elif o in ("-t", "--test-count"):
			g_test_count = int(a)

def checkOpt():
	if not g_package:
		print '-p or --package. Package name should not be null'
		sys.exit(1)
	if not g_activity:
		print '-a or --acitivity. Acitivity name should not be null'
		sys.exit(1)
	if g_test_count <= 0:
		print '-t or --test-count. Test count should large than 0'
		sys.exit(1)
	return True

if __name__ == '__main__':
	intOpt()
	checkOpt()
	doTest()
