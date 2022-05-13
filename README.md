# background-removal

Rodan does not like hyphens, so I changed the name from `background-removal` to `background_removal`.

Put this repository under `<rodan repository, develop branch>/rodan-main/code/rodan/jobs`

### Register a new job
`<rodan repository, develop branch>/rodan-main/code/rodan/jobs/register_all_jobs.py:register_py3()`
`

Add this inside `def register_gpu()`:
``` Python
    try:
        from rodan.jobs.background_removal.BgRemovalRodan import BgRemoval
        app.register_task(BgRemoval())
    except Exception as exception:
        import_name = "BgRemoval"
        print(import_name + " failed to import with the following error:", exception.__class__.__name__)
```

### Update `settings.py`
`<repository, develop branch>/rodan-main/code/rodan/settings.py`

Add `rodan.jobs.background_removal` to `RODAN_GPU_JOBS`.

Should look like this:
``` Python
RODAN_GPU_JOBS = [
    "rodan.jobs.Calvo_classifier",
    "rodan.jobs.text_alignment",
    "rodan.jobs.background_removal"
]
```

### Install `opencv-python==4.5.5.64` inside `gpu-celery` container

`requirements.txt` lists required packages, but basically you only need to install `opencv-python==4.5.5.64`.

```
docker-compose exec gpu-celery bash
```

```
pip install opencv-python==4.5.5.64
```

--- 
Basically these two versions:
```
opencv-python==3.4.2.17 # from Calvo_classifier/requirements.txt
opencv-python-headless==4.5.5.64
```
cause the error message
```shell
Traceback (most recent call last):
  File "/usr/local/lib/python3.7/dist-packages/celery/app/trace.py", line 412, in trace_task
    R = retval = fun(*args, **kwargs)
  File "/usr/local/lib/python3.7/dist-packages/celery/app/trace.py", line 704, in __protected_call__
    return self.run(*args, **kwargs)
  File "/code/Rodan/rodan/jobs/base.py", line 771, in run
    retval = self.run_my_task(inputs, settings, arg_outputs)
  File "/code/Rodan/rodan/jobs/background_removal/BgRemovalRodan.py", line 50, in run_my_task
    from . import background_removal_engine as Engine
  File "/code/Rodan/rodan/jobs/background_removal/background_removal_engine.py", line 6, in <module>
    import cv2
  File "/usr/local/lib/python3.7/dist-packages/cv2/__init__.py", line 9, in <module>
    from .cv2 import _registerMatType
ImportError: cannot import name '_registerMatType' from 'cv2.cv2' (/usr/local/lib/python3.7/dist-packages/cv2/cv2.cpython-37m-x86_64-linux-gnu.so)
```
The error message shows up whenever there's a job trying to load `cv2` inside `gpu-celery`. So even if you do not register `Calvo_classifier` but register `background_removal (this repo)`, the error message is still there.

Upgrade `opencv-python` to s.t. its version matches `opencv-python-headless` solves the error.