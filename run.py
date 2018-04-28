import subprocess as sp
import glob

""" SETUP """
HiGHS = '/home/sascha/Downloads/HiGHS/build/bin/highs'          # PATH to binary
NETLIB_MPS_DIR = '/home/sascha/Documents/HiGHS_eval/netlib'     # PATH to folder of .mps files

                                        # 2 configurations:
CONFIGS = [[''],                        #   default
           ['-p', 'On']                 #   default + presolve On
          ]

TIMEOUT_SECS = 30                       # TIMEOUT is treated as error!

""" Helper function """
def solve_HiGHS(instance_fp, config):
    status = True
    timeout = False
    res = None

    try:
        res = sp.run([HiGHS] + config + ['-f', instance_fp], timeout=TIMEOUT_SECS,
                 stdout=sp.PIPE, stderr=sp.PIPE)
    except sp.TimeoutExpired:
        status = False
        timeout = True

    if status:
        try:
            res.check_returncode()
        except sp.CalledProcessError:
            status = False

    if timeout:
        return (status, instance_fp, 'TIMEOUT', config, -999, b'', b'')#
    elif not status:
        return (status, instance_fp, 'SOLVER ERROR', config, res.returncode, res.stdout, res.stderr)
    else:
        return (status, instance_fp, '', config, res.returncode, res.stdout, res.stderr)

""" Test all """
INSTANCES = glob.glob(NETLIB_MPS_DIR + '/*.mps')
N_RUNS = len(INSTANCES) * len(CONFIGS)
RESULTS = []

run = 1
print('----------------')
print('Run all {} tests...'.format(N_RUNS))
for instance in INSTANCES:
    for config in CONFIGS:
        print('run {}/{}'.format(run, N_RUNS))
        run += 1
        RESULTS.append(solve_HiGHS(instance, config))
print('    ...all tests finished!')

""" Print erroneous runs """
print('-------------------')
print('Check for errors...')
for r in RESULTS:
    if not r[0]:
        reformatted_stdout = "\n".join(map(lambda x: '        ' + x, r[5].decode('utf-8').split('\n')))
        reformatted_sterr = "\n".join(map(lambda x: '        ' + x, r[6].decode('utf-8').split('\n')))

        print('Observed error:')
        print('    Instance: {}'.format(r[1]))
        print('    Arguments: {}'.format(r[3]))
        print('    Error-type: {}'.format(r[2]))
        print('    -> returncode: {}'.format(r[4]))
        print('    -> stdout:\n\n{}\n'.format(reformatted_stdout))
        print('    -> stderr:\n\n{}\n'.format(reformatted_sterr))
print('    ...all checks finished!')
