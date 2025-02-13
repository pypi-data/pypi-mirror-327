import time

import pytest
from crow_client.clients.rest_client import RestClient


@pytest.mark.timeout(300)
@pytest.mark.flaky(reruns=3)
@pytest.mark.skip(reason="Temporary skip until queue is working")
def test_paperqa_job():
    client = RestClient()
    job_data = {
        "name": "job-futurehouse-dummy-env",
        "query": "How many moons does earth have?",
    }
    client.create_job(job_data)

    # The job will return an object if there's only one frame, or one state.
    # After more are added, job will return several status checks, one per frame / state stored
    # If any are in progress, we wait
    while any(
        (job_status := j["status"]) == "in progress"
        for j in (
            [client.get_job()]
            if isinstance(client.get_job(), dict)
            else client.get_job()
        )
    ):
        time.sleep(5)

    assert job_status == "success"
