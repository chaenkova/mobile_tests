import allure
import config
import os


def attach_bstack_video(session_id):
    import requests
    bstack_session = requests.get(
        f'https://api.browserstack.com/app-automate/sessions/{session_id}.json',
        auth=(os.getenv('bstack_userName'), os.getenv('bstack_accessKey')),
    ).json()
    print(bstack_session)
    video_url = bstack_session['automation_session']['video_url']

    allure.attach(
        '<html><body>'
        '<video width="100%" height="100%" controls autoplay>'
        f'<source src="{video_url}" type="video/mp4">'
        '</video>'
        '</body></html>',
        name='video recording',
        attachment_type=allure.attachment_type.HTML,
    )


def path_from_project(relative_path: str):
    import selene_in_action
    from pathlib import Path

    return (
        Path(selene_in_action.__file__)
        .parent.parent.joinpath(relative_path)
        .absolute()
        .__str__()
    )
