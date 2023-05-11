import re

def prep_docker_ubuntu(http, tcp):
    print(http)
    print(tcp)
    
    with open('setup.sh', 'r') as f:
        file_str = f.read()


    patterns = [
        (r'server\s*=\s*.*$', f'server="http://127.0.0.1:{http}"'),
        (r'socket\s*=\s*.*$', f'socket="127.0.0.1:{tcp}"') 
    ]

    for pattern, replacement in patterns:
        file_str = re.sub(pattern, replacement, file_str, flags=re.MULTILINE)

#Write the modified string back to the setup.sh file
    with open('setup.sh', 'w') as f:
        f.write(file_str)


prep_docker_ubuntu(8888,7010)
# import re

# with open('setup.sh', 'r') as f:
#     file_str = f.read()

# http = 12345
# tcp = 12345

# patterns = [
#     (r'server\s*=\s*.*$', f'server="http://127.0.0.1:{http}"'),
#     (r'socket\s*=\s*.*$', f'socket="127.0.0.1:{tcp}"') 
# ]


# for pattern, replacement in patterns:
#     file_str = re.sub(pattern, replacement, file_str, flags=re.MULTILINE)

# # Write the modified string back to the setup.sh file
# with open('setup.sh', 'w') as f:
#     f.write(file_str)
