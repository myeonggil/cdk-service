
# Welcome to your CDK Python project!

This is a blank project for Python development with CDK.

The `cdk.json` file tells the CDK Toolkit how to execute your app.

This project is set up like a standard Python project.  The initialization
process also creates a virtualenv within this project, stored under the `.venv`
directory.  To create the virtualenv it assumes that there is a `python3`
(or `python` for Windows) executable in your path with access to the `venv`
package. If for any reason the automatic creation of the virtualenv fails,
you can create the virtualenv manually.

To manually create a virtualenv on MacOS and Linux:

```
$ python3 -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .venv\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```

To add additional dependencies, for example other CDK libraries, just add
them to your `setup.py` file and rerun the `pip install -r requirements.txt`
command.

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

Enjoy!


# 간단한 팁
## 1. brew를 통해 cdk 설치
```bash
brew install aws-cdk
```
## 2. CDK가 인식할 수 있도록 profile 이름을 명시
```bash
aws configure --profile {name}
```
## 3. 명확한 profile에서 작업 수행할 수 있도록 profile 명시
```bash
cdk diff --profile {name}
```

# workflow
## 1. app.py
```text
cdk가 처음 실행되는 파일로 시작할 스택 정보를 등록
```

```python
env_info = core.Environment(account='#', region='ap-northeast-2') # AWS account 정보와 region

app = core.App()
CdkServiceStack(app, "cdkService", env=env_info) # "cdkService"라는 이름의 스택을 생성

app.synth() # cdk.out에 생성된 template과 sync를 비교

```