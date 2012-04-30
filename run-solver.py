#!/usr/bin/env python2

import sys

def usage():
    print 'usage: solver directory'
    print 'options: -h, -e extension, -p prefix_name, -t timeout, -m memout, -f (force log removal) -n'

if len( sys.argv ) < 2 :
    usage()
    sys.exit(0)

import os, glob, getopt, shutil

extension = '.cnf'
job_name_prefix = ''
timeout = '1800'
memout = '4G'
removedir = False
resources = ' -V '#-pe smp 4 '
#resources = ' -V -pe smp 4 '
grow = None

try:
    opts, args = getopt.getopt(sys.argv[1:], "he:p:t:m:f:g:", ["help", "extension", "prefix", "timeout", "memout", "force", "grow"])
except getopt.GetoptError, err:
    print str(err) # will print something like "option -a not recognized"
    usage()
    sys.exit(2)
for o, a in opts:
    if o in ("-e", "--extension"):
        extension = a
    elif o in ("-p", "--prefix"):
        job_name_prefix = a
    elif o in ("-t", "--timeout"):
            timeout = a
    elif o in ( "-m", "--memout" ):
        memout = a
    elif o in ("-f", "--force"):
        removedir = True
    elif o in ("-g", "--grow"):
        grow = a
    elif o in ("-h", "--help"):
        usage()
        sys.exit()
    else:
        assert False, "unhandled option"

solver = os.path.abspath( args[0] )
directory = os.path.expanduser( args[1] )
if not directory.endswith('/'):
   directory += '/'
log_dir = os.path.expanduser( os.getcwd() + '/log/' ) + job_name_prefix + os.path.basename( solver ) + '.' + directory.split('/')[-2]

if grow is not None:
    solver += ' -grow=' + grow
    log_dir += '.' + grow
print 'Current parameters:\n' + 'Solver: ' + solver + "\nDirectori: " + directory + "\nExtension: " + extension + "\nJob Prefix: " + job_name_prefix + "\nLog dir: " + log_dir + "\nMemory out: " + memout + "\nTime out: " + timeout

if removedir :
   shutil.rmtree( log_dir )

#if os.path.isdir( log_dir ):
#    print 'Error: Log directory already exists'
#    print 'It can be removed it with: rm -R ' + log_dir
#    sys.exit(0)

files = glob.glob( directory + "/*" + extension )
if len( files ) == 0:
    print 'Error: no files'
    sys.exit(0)

if not os.path.isdir (log_dir):
    os.makedirs( log_dir )
    
for file in glob.glob( directory + "/*" + extension ):
    file_basename = os.path.basename( file )
    log = log_dir + '/' + file_basename + '.log'
    cmd = ('timelimit -p -s 2 -t ' + timeout + ' ' + solver + ' ' + file + '>' + log)
    print(cmd + '\n')
    #import pdb; pdb.set_trace()
    if not os.path.exists(log):
        print('log file not exist.\n')
        os.system(cmd)
    #print ('echo /usr/bin/time -p ' + solver + ' ' + file + ' | qsub ' + resources + ' -cwd -o ' + log_dir + '/' + file_basename + '.log -j y -n ' + job_name_prefix + os.path.basename( solver ) + '.' + file_basename + ' > /dev/null ')
    #break
    #os.system('echo /usr/bin/time -p ' + solver + ' ' + file + ' | qsub ' + resources + ' -cwd -o ' + log_dir + '/' + file_basename + '.log -j y -n ' + job_name_prefix + os.path.basename( solver ) + '.' + file_basename + ' > /dev/null ')
    #os.system('echo /usr/bin/time -p ' + solver + ' ' + file + " | qsub " + resources + " -l h_cpu=" + timeout + " -l h_vmem=" + memout + " -l mem=" + memout +  " -o " + log_dir + '/' + file_basename + '.log -j y -N ' + job_name_prefix + os.path.basename( solver ) + '.' + file_basename + ' > /dev/null ')
    #cmd = ('echo /usr/bin/time -p ' + solver + ' ' + file + " | qsub " + resources + " -l cput=" + timeout + " -l vmem=" + memout + " -l mem=" + memout +  " -o " + log_dir + '/' + file_basename + '.log -j oe -N ' + job_name_prefix + os.path.basename( solver ) + '.' + file_basename + ' > /dev/null ')
    #print cmd
    #os.system(cmd)

