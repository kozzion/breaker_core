import os
import sys
from pathlib import Path
from paramiko import SSHClient
import scp

class DockerConfig(object):
    
    def __init__(self, name_image, name_container, path_file_config_source, path_file_config_target, path_file_dockerfile_source, path_file_dockerfile_target) -> None:
        super().__init__()
        self.name_image = name_image 
        self.name_container = name_container
        self.path_file_config_source = path_file_config_source
        self.path_file_config_target = path_file_config_target
        self.path_file_dockerfile_source = path_file_dockerfile_source
        self.path_file_dockerfile_target = path_file_dockerfile_target
        

    def print_log(self) -> None:
        command = 'docker logs ' + self.name_container
        self.execute(command)

    def stop(self) -> None:
        command = 'docker stop ' + self.name_container
        self.execute(command)

    def remove_container(self) -> None:
        command = 'docker rm ' + self.name_container
        self.execute(command)

    def remove_image(self) -> None:
        command =  'docker rmi ' + self.name_image
        self.execute(command)

    def build(self) -> None:
        command =  'docker build'
        command += ' -t ' + self.name_image
        command += ' -f ' + self.path_file_dockerfile_target
        command += ' .'
        self.execute(command)

    def restart(self):  
        self.stop()
        self.remove_container()
        self.run()

    def run(self) -> None:
        command =  'docker run'
        command += ' -d' #run detached
        command += ' --name ' + self.name_container
        command += ' --mount type=bind,source=' + self.path_file_config_target + ',target=/config/config.cfg,readonly' 
        command += ' ' + self.name_image
        self.execute('command')

    def execute(self, command):
        raise NotImplementedError()

class DockerConfigSSH(DockerConfig):

    def __init__(self, client_ssh, name_image:str, name_container:str, path_file_config_source, path_file_config_target, path_file_dockerfile_source, path_file_dockerfile_target) -> None:
        super().__init__(name_image, name_container, path_file_config_source, path_file_config_target, path_file_dockerfile_source, path_file_dockerfile_target)
        self.client_ssh = client_ssh

    def set_config(self, path_file_config_source:str):
        client_scp = scp.SCPClient(self.client_ssh.get_transport())
        client_scp.put(path_file_config_source, self.path_file_config_target)

    def set_dockerfile(self, path_file_dockerfile_source:str):
        client_scp = scp.SCPClient(self.client_ssh.get_transport())
        client_scp.put(path_file_dockerfile_source, self.path_file_dockerfile_target)

    def deploy(self):
        self.set_config(self.path_file_config_source)
        self.set_dockerfile(self.path_file_dockerfile_source)

        self.stop()
        self.remove_container()
        self.remove_image()
        self.build()
        self.run()

    def execute(self, command):
        print(command)
        sys.stdout.flush()
        stdin, stdout, stderr=self.client_ssh.exec_command(command)
        while True:
            v = stdout.channel.recv(1024)
            if not v:
                break            
            r = stderr.channel.recv(1024)
            sys.stdout.write(v)
            if r:
                sys.stdout.write(r)
            sys.stdout.flush()
        # print()
        # print('STDOUT')
        # for line in stdout.readlines():
        #     print(line.encode("utf-8").decode('utf8')[:-1])
        # sys.stdout.flush()
        # print()
        # print('STDERR')
        # for line in stderr.readlines():
        #     print(line.encode("utf-8").decode('utf8')[:-1])
        # sys.stdout.flush()

    @staticmethod
    def from_dict(client_ssh, dict_config_docker:dict) -> 'DockerConfigSSH':
        return DockerConfigSSH(
            client_ssh,
            dict_config_docker['name_image'],
            dict_config_docker['name_container'],
            dict_config_docker['path_file_dockerfile_source'],
            dict_config_docker['path_file_dockerfile_target'],
            dict_config_docker['path_file_config_source'],
            dict_config_docker['path_file_config_target'])
        

class DockerConfigCmd(DockerConfig):
    def __init__(self, name_image:str, name_container:str) -> None:
        super().__init__(name_image, name_container)
        # self.path_file_dockerfile_target_target = path_file_dockerfile_target 
        # self.path_file_config_target_target = path_file_dockerfile_target

    def set_config(self, path_file_config_source:str):
        client_scp = scp.SCPClient(self.client_ssh.get_transport())
        client_scp.put(path_file_config_source, self.path_file_config_target_target)




    def execute(self, command):
        print(command)
        os.system(command)

class ToolsDocker:
    @staticmethod
    def ssh_stop(client_ssh:SSHClient, name_container:str) -> None:
        # stop container
        command =  'docker stop ' + name_container
        print(command)
        sys.stdout.flush()
        stdin, stdout, stderr = client_ssh.exec_command(command)
        print('\n'.join(stdout.readlines()).encode("utf-8"))
        print('\n'.join(stderr.readlines()).encode("utf-8"))
        sys.stdout.flush()
        
    @staticmethod
    def ssh_remove_container(client_ssh:SSHClient, name_container:str) -> None:
        # unname container
        command =  'docker rm ' + name_container
        print(command)
        sys.stdout.flush()
        stdin, stdout, stderr = client_ssh.exec_command(command)
        print('\n'.join(stdout.readlines()).encode("utf-8"))
        print('\n'.join(stderr.readlines()).encode("utf-8"))
        sys.stdout.flush()

    @staticmethod
    def ssh_remove_image(client_ssh:SSHClient, name_image:str) -> None:
        command =  'docker rmi ' + name_image
        print(command)
        sys.stdout.flush()
        stdin, stdout, stderr = client_ssh.exec_command(command)
        print('\n'.join(stdout.readlines()).encode("utf-8"))
        print('\n'.join(stderr.readlines()).encode("utf-8"))
        sys.stdout.flush()
        
    @staticmethod
    def ssh_build(client_ssh:SSHClient, name_image:str, path_file_dockerfile_target:str) -> None:
        command =  'docker build'
        command += ' -t ' + name_image
        command += ' -f ' + path_file_dockerfile_target
        command += ' .'
        print(command)
        sys.stdout.flush()
        stdin,stdout,stderr=client_ssh.exec_command(command)
        print('\n'.join(stdout.readlines()).encode("utf-8"))
        print('\n'.join(stderr.readlines()).encode("utf-8"))
        sys.stdout.flush()

    
    @staticmethod
    def ssh_run(client_ssh:SSHClient, name_container:str, name_image:str, path_file_config_target:str) -> None:
        command =  'docker run'
        command += ' -d' #run detached
        command += ' --name ' + name_container
        command += ' --mount type=bind,source=' + path_file_config_target + ',target=/config/config.cfg,readonly' 
        command += ' ' + name_image
        print(command)
        sys.stdout.flush()
        stdin,stdout,stderr=client_ssh.exec_command(command)
        print('\n'.join(stdout.readlines()).encode("utf-8"))
        print('\n'.join(stderr.readlines()).encode("utf-8"))
        sys.stdout.flush()

    @staticmethod
    def ssh_print_log(client_ssh:SSHClient, name_image, name_container):
        return 'docker logs ' + name_container

    @staticmethod
    def deploy(client_ssh:SSHClient, 
        name_image:str,
        name_container:str,
        path_file_config_source:str, 
        path_file_config_target:str, 
        path_file_dockerfile_source:str, 
        path_file_dockerfile_target:str):
 

        client_scp = scp.SCPClient(client_ssh.get_transport())
        client_scp.put(path_file_config_source, path_file_config_target)
        client_scp.put(path_file_dockerfile_source, path_file_dockerfile_target)

        ToolsDocker.ssh_stop(client_ssh, name_container)
        ToolsDocker.ssh_remove_container(client_ssh, name_container)
        ToolsDocker.ssh_remove_image(client_ssh, name_image)
        ToolsDocker.ssh_build(client_ssh, name_image, path_file_dockerfile_target)
        ToolsDocker.ssh_run(client_ssh, name_container, name_image, path_file_config_target)

    @staticmethod    
    def ssh_restart(client_ssh:SSHClient, name_image, name_container, path_file_config_target:str):  
        ToolsDocker.ssh_stop(client_ssh, name_container)
        ToolsDocker.ssh_remove_container(client_ssh, name_container)
        ToolsDocker.ssh_run(client_ssh, name_container, name_image, path_file_config_target)


    @staticmethod    
    def test(name_image:str, name_container:str, path_file_config:Path, path_file_dockerfile:Path):
        # stop container
        command =  'docker stop ' + name_container
        print(command)
        os.system(command)

        # unname old container
        command =  'docker rm ' + name_container
        print(command)
        os.system(command)

        # unname old image #TODO do we need this?
        command =  'docker rmi ' + name_image
        print(command)
        os.system(command)

        # build new image
        if not path_file_dockerfile.exists():
            raise Exception('missing dockerfile: ' + str(path_file_dockerfile))
        command =  'docker build'
        command += ' -t ' + name_image
        command += ' -f ' + str(path_file_dockerfile.absolute())
        command += ' .'
        print(command)
        sys.stdout.flush()
        os.system(command)
 
        
        command =  'docker run'
        command += ' --name ' + name_container
        command += ' --mount type=bind,source=' + str(path_file_config.absolute()) + ',target=/config/config.cfg,readonly' 
        command += ' ' + name_image
        print(command)
        sys.stdout.flush()
        os.system(command)
        