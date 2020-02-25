

import os
from subprocess import PIPE, run




class Openssl(object):

    def __init__(self, config_file):
        if not os.path.exists(config_file):
            raise Exception("openssl.cnf file not found (expected {})".format(config_file))
        self._config_file = config_file
      



    def openssl_rand(self, directory):
        random_rn_file = os.path.join(directory, "random.rnd" )
        if not os.path.exists(random_rn_file):
            command = [ "openssl", "rand", "-out", random_rn_file, "20" ]
            print("executing command: ", " ".join(command), flush=True)
            result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True)
            print("result.stdout: ", result.stdout, "result.stderr: ", result.stderr, flush=True)

            if result.returncode != 0:
                raise Exception("openssl rand failed")
    
        if not os.path.exists("/root/.rnd"):
            os.symlink(random_rn_file, "/root/.rnd")

        return random_rn_file


    def openssl_genrsa(self, output_filename):
        command = ["openssl", "genrsa" , "-out", output_filename, "2048"]
        print("executing command: ", " ".join(command), flush=True)

        result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True)
        
        print("result.stdout: ", result.stdout, "result.stderr: ", result.stderr, flush=True)

        if result.returncode != 0:
            raise Exception("openssl genrsa failed")


    # create a request
    def openssl_req_request(self, commonname, random_filename, key_pem_filename, request_filename):

        subject = "/CN={}/O=server/".format(commonname)

        command = ["openssl", "req", \
                "-rand", random_filename,
                "-new", \
                "-key", key_pem_filename, \
                "-out", request_filename, \
                "-outform", "PEM", \
                "-subj", subject , \
                "-nodes"]
        print("executing command: ", " ".join(command), flush=True)

        result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True)
        
        print("result.stdout: ", result.stdout, "result.stderr: ", result.stderr, flush=True)

        if result.returncode != 0:
            raise Exception("openssl req failed")

        return


    def openssl_ca(self, openssl_config_file, request_filename, certificate_file):

        #openssl ca -config openssl.cnf -in ${SSL_DIR}/server/req.pem -out \
        #	${SSL_DIR}/server/cert.pem -notext -batch -extensions server_ca_extensions

        command = ["openssl", "ca", \
                    "-config", openssl_config_file, \
                    "-in", request_filename, \
                    "-out", certificate_file, \
                    "-notext", \
                    "-batch", \
                    "-extensions", "server_ca_extensions" ]
        print("executing command: ", " ".join(command), flush=True)

        result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True)
        
        print("result.stdout: ", result.stdout, "result.stderr: ", result.stderr, flush=True)

        if result.returncode != 0:
            raise Exception("openssl ca failed")

        return