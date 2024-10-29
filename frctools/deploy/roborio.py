from frctools.network.ssh import SshConnection, SshExecResult

import pathlib


def deploy_rio(team_number: int, robot_code_path: str = './robot/'):
    team_str = str(team_number)

    if len(team_str) <= 2:
        address = f'10.0.{team_str}.2'
    else:
        address = f'10.{team_str[:-2]}.{team_str[-2:]}.2'

    home_dir = pathlib.PurePosixPath('/home/lvuser')
    py_deploy_dir = home_dir / 'py'
    py_deploy_temp_dir = home_dir / 'py_temp'

    with SshConnection(address, 'lvuser', '') as client:
        deployed_cmd = (
            'env LD_LIBRARY_PATH=/usr/local/frc/lib/ '
            f'/usr/local/bin/python3 -u -O -m robotpy --main {py_deploy_dir}/robot.py run'
        )
        deployed_cmd_filename = 'robotCommand'
        bash_cmd = '/bin/bash -ce'

        replace_cmd = f'rm -rf {py_deploy_dir}; mv {py_deploy_temp_dir} {py_deploy_dir}'

        try:
            client.exec_cmd(
                cmd=f'echo "{deployed_cmd}" > {home_dir}/{deployed_cmd_filename}; mkdir -p {py_deploy_temp_dir}',
                check=True,
                print_output=True
            )
        except Exception as e:
            print(e)
            return None

        try:
            client.put_scp(robot_code_path, f'{py_deploy_temp_dir}', recursive=True)
        except Exception as e:
            print(e)
            return None

        sshcmd = (
            f"{bash_cmd} '"
            f"/home/admin/rpip install --force-reinstall --no-deps -r {py_deploy_temp_dir}/requirements-roborio.txt; "
            f"{replace_cmd};"
            f"/usr/local/bin/python3 -O -m compileall -q -r 5 /home/lvuser/py;"
            ". /etc/profile.d/frc-path.sh; "
            ". /etc/profile.d/natinst-path.sh; "
            f"chown -R lvuser:ni {py_deploy_dir}; "
            "sync; "
            "/usr/local/frc/bin/frcKillRobot.sh -t -r || true"
            "'"
        )

        try:
            client.exec_cmd(sshcmd,
                            check=True,
                            print_output=True)
        except Exception as e:
            print(e)
            return None

        print('Success!')
