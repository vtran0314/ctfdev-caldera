import subprocess
import re

dockerImages = subprocess.check_output(['docker', 'images', '-a']).decode('utf-8')
print(dockerImages)
dockerImages_nums = [
    int(re.search(r'^ubuntuimages-(\d+)', d).group(1))
    for d in dockerImages.split('\n')
    if re.match(r'^ubuntuimages-\d+', d)
]
# dockerImages_nums = [int(d.split('-')[1]) for d in dockerImages.split('\n') if re.match(r'ubuntuimages-\d+', d)]

# dockerImages_nums = [int(d.split('-')[1]) for d in dockerImages.split('\n') if d.startswith('ubuntuimages-')]
print(dockerImages_nums)
if len(dockerImages_nums) == 0:
    next_num = 1
    next_img = f'ubuntuimages-{next_num}'
    dockerBuild = f'docker build -t {next_img}:latest .'
    print(dockerBuild)
    subprocess.Popen(dockerBuild.split(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).wait()

    dockerRun = f'docker run -d {next_img}:latest'
    print(dockerRun)
    subprocess.run(dockerRun.split(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

else:
    next_num = max(dockerImages_nums) + 1
    next_img = f'ubuntuimages-{next_num}'
    dockerBuild = f'docker build -t {next_img}:latest .'
    print(dockerBuild)
    subprocess.Popen(dockerBuild.split(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).wait()

    dockerRun = f'docker run -d {next_img}:latest'
    print(dockerRun)
    subprocess.run(dockerRun.split(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
