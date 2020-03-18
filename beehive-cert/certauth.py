import os
from subprocess import PIPE, run
import openssl
import time

class CertificateAuthority(object):
    def __init__(self, openssl, directory):

        self._directory = directory
        self._openssl = openssl

        self.create_ca_authority_directory()

        self.create_ca_key_if_needed()

        self.create_ca_cert_if_needed()


    def create_ca_key_if_needed(self):
	
        ca_key_file = os.path.join(self._directory,"private/cakey.pem" )
        if os.path.exists(ca_key_file):
            print("CA key already exists.", flush=True)
            return


        print("Creating CA key ...", flush=True)


        try:
            self._openssl.openssl_genrsa(ca_key_file)
        except Exception as e:
            raise e

        

        # Is that needed ?
        #	rm -f $CA_DIR/cacert.pem 
        #	rm $CA_DIR/certs/*
        return

    def create_ca_cert_if_needed(self):
    
        cacert_pem_file = os.path.join(self._directory,"cacert.pem" )
        cakey_file = os.path.join(self._directory,"private/cakey.pem" )



        if os.path.exists(cacert_pem_file):
            print("CA certificate already exists.", flush=True)
            return



        self._openssl.openssl_rand(self._directory)



        print("Creating CA certificate...", flush=True)
        
        #-x509 outputs a self signed certificate instead of a certificate request.

        command = ["openssl", "req", "-new", \
                "-x509" , \
                "-key", cakey_file, \
                "-days", "3650", \
                "-out", cacert_pem_file, \
                "-outform", "PEM", \
                "-subj", "/CN=waggleca/", \
                "-sha256"]
        print("executing command: ", " ".join(command), flush=True)

        result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True)
        
        print("result.stdout: ", result.stdout, "result.stderr: ", result.stderr, flush=True)

        if result.returncode != 0:
            raise Exception("openssl req failed")

        return





    def create_ca_authority_directory(self):
        if not os.path.exists(self._directory):
            try:
                print("creating {} ...".format(self._directory), flush=True)
                os.mkdir(self._directory)
            except OSError as e:
                
                raise Exception("Creation of the directory {} failed: {}".format(self._directory, str(e) ))
            
        os.chmod(self._directory, 0o755)


        for subdir in ["certs","private"]:
            subdir_full = os.path.join(self._directory, subdir)
            print("creating {} ...".format(subdir_full), flush=True)
            if not os.path.exists(subdir_full):
                os.mkdir(subdir_full)
            os.chmod(subdir_full, 0o700)

        serial_file=os.path.join(self._directory, "serial")
        if not os.path.exists(serial_file):
            print("creating serial file {} ...".format(serial_file), flush=True)
            with open(serial_file, 'a') as out:
                out.write('echo 01\n')
        
        index_file=os.path.join(self._directory, "index.txt")
        if not os.path.exists(index_file):
            print("creating empty index file {} ...".format(index_file), flush=True)
            with open(index_file, 'a') as out:
                None



        index_attr_file = os.path.join(self._directory, "index.txt.attr")
        # this is needed for "node" certificates. We may change that later.
        if not os.path.exists(index_attr_file):
            print("creating index_attr_file {} ...".format(index_attr_file), flush=True)
            with open(index_attr_file, 'a') as out:
                out.write('unique_subject = no\n')
        

        

        return




