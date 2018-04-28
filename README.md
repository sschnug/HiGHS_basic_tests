# Introduction
This is a small testing-code, which currently does:

- check: [HiGHS](https://github.com/ERGO-Code/HiGHS) Linear-Programming solver
- against: [netlib lp dataset](http://www.netlib.org/lp/data/index.html)

"Checking" means:

- use a precompiled binary of ```HiGHS```
- call above binary on the specific ```_instance_.mps``` file
- checks:
  - the returned status-code
    - every code != 0 is an error
  - if some timeout-limit was reached
    - timeout is treated as error

There is (currently) no check in regards to the ```optimum``` nor ```feasibility```!
Incorporating this probably could be based on the results given by:

> Koch, Thorsten. "The final NETLIB-LP results." Operations Research Letters 32.2 (2004): 138-142.

# Requirements
The code was only tested using **Python 3**.

# Preparation

## Prepare netlib dataset
The following will download all mps-files given in: ```http://www.zib.de/koch/perplex/data/netlib/mps/```. These are the files (4 instances dropped: compare ```netlib/stats.txt``` with above link or the prepared ```netlib/links.txt```) used in above citation.

The bash-script needs ```wget``` and ```gunzip``` available in path.

    cd netlib
    ./get_mps.sh
    cd ..

## Set configuration in run.py

    HiGHS = '/home/sascha/Downloads/HiGHS/build/bin/highs'          # PATH to binary
    NETLIB_MPS_DIR = '/home/sascha/Documents/HiGHS_eval/netlib'     # PATH to folder of .mps files

                                            # 2 configurations:
    CONFIGS = [[''],                        #   default
               ['-p', 'On']                 #   default + presolve On
              ]

    TIMEOUT_SECS = 30                       # TIMEOUT is treated as error!

## Run

    python3 run.py

## Observe printed output
Example:

    sascha@sascha-VirtualBox:~/Documents/HiGHS_eval$ python3 run.py
    ----------------
    Run all 188 tests...
    run 1/188
    run 2/188
    ... (omitted in example)
    run 188/188
        ...all tests finished!
    -------------------
    Check for errors...
    Observed error:
        Instance: /home/sascha/Documents/HiGHS_eval/netlib/greenbea.mps
        Arguments: ['-p', 'On']
        Error-type: SOLVER ERROR
        -> returncode: -6
        -> stdout:

            Presolve is set to On
            Reading file /home/sascha/Documents/HiGHS_eval/netlib/greenbea.mps
            Setting default value crashMode = Off
            Setting default value edWtMode = DSE1
            ====================================================================================
            Running HiGHS
            ------
            Error during presolve: no variable found in singleton row 281.

        -> stderr:

            terminate called after throwing an instance of 'std::out_of_range'
              what():  vector::_M_range_check: __n (which is 18446744073709551615) >= this->size() (which is 30877)


    Observed error:
        Instance: /home/sascha/Documents/HiGHS_eval/netlib/cycle.mps
        Arguments: ['-p', 'On']
        Error-type: TIMEOUT
        -> returncode: -999
        -> stdout:



        -> stderr:



    Observed error:
        Instance: /home/sascha/Documents/HiGHS_eval/netlib/greenbeb.mps
        Arguments: ['-p', 'On']
        Error-type: SOLVER ERROR
        -> returncode: -6
        -> stdout:

            Presolve is set to On
            Reading file /home/sascha/Documents/HiGHS_eval/netlib/greenbeb.mps
            Setting default value crashMode = Off
            Setting default value edWtMode = DSE1
            ====================================================================================
            Running HiGHS
            ------
            Error during presolve: no variable found in singleton row 281.

        -> stderr:

            terminate called after throwing an instance of 'std::out_of_range'
              what():  vector::_M_range_check: __n (which is 18446744073709551615) >= this->size() (which is 30877)


        ...all checks finished!
