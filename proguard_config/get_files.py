import random
import time
import base64
import os
from github import Github

tokens = "e7ede07fc5813d7ebe64de38ec9bd9f9a2be6fd3"

class ProguardConfigFile:

    def __init__(self, root_path):
        self.root_path = root_path
        self.github = Github(tokens)
        self.visited_file = open('visited1.txt', 'a+')
        self.visited = []

    def search(self):
        proguard_config_files = self.github.search_code(
            query='This is a configuration file for ProGuard',
            # sort="stars",
            # order="desc",
            **{
                'in': 'file',
                'extension': 'txt'
                # 'type': 'code'
                # "stars": str(self.min_stars) + ".." + str(self.max_stars),
                # "archived": "false",
                # "license": "apache-2.0",
                # "fork": "false",
            }
        )
        return proguard_config_files

    def get_1000_config_files(self):
        """
        **{'language': 'java', "stars": ">=1500", "archived": "false", "license": "apache-2.0", "fork": "false"})
        """
        config_files = self.search()
        print(config_files.totalCount)
        for file in config_files:
            if file.html_url in self.visited:
                continue
            self.visited.append(file.html_url)
            self.visited_file.write(file.html_url+'\n')
            content = base64.b64decode(file.content)
            # file_path = "{}/{}.txt".format(self.root_path, file.sha)
            file_path  = '{}/{}.txt'.format(self.root_path, self.index)
            with open(file_path, "w") as f:
                f.write(content)
            self.index += 1

            print(self.index, file.html_url)
            time.sleep(4 + random.random() / 10)

    def save_repo_list(self):
        lines = self.visited_file.readlines()
        for line in lines:
            self.visited.append(line.rstrip('\n'))
        self.index = len(self.visited)
        for i in range(1000): # 6
            print("step %d" % (i + 1))
            self.get_1000_config_files()
            time.sleep(10 + random.random() * 5)


if __name__ == "__main__":
    path = 'config_files1'
    is_exist = os.path.exists(path)
    if not is_exist:
        os.makedirs(path)
    else:
        pass
    progurad_config_file = ProguardConfigFile(path)
    progurad_config_file.save_repo_list()