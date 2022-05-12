# background-removal

Rodan does not like hyphens, so I changed the name from `background-removal` to `background_removal`.

Put this repository under `<rodan repository, develop branch>/rodan-main/code/rodan/jobs`

### Register a new job
`<rodan repository, develop branch>/rodan-main/code/rodan/jobs/register_all_jobs.py:register_py3()`
`

Add this inside `def register_py3()`:
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

Add `rodan.jobs.background_removal` to `RODAN_PYTHON3_JOBS`.

Should look like this:
``` Python
RODAN_PYTHON3_JOBS = [
    "rodan.jobs.helloworld",
    "rodan.jobs.hpc_fast_trainer",
    "rodan.jobs.pil_rodan",
    "rodan.jobs.mei2vol_wrapper",
    "rodan.jobs.background_removal"
]
```

### Install `opencv-python==4.5.5.64` and `scikit-image==0.19.2` inside `py3-celery` container

`requirements.txt` lists required packages, but basically you only need to install `opencv-python` and `scikit-image` and they'll install the rest for you.

```
docker-compose exec py3-celery bash
```

```
pip install scikit-image==0.19.2
```

```
pip install opencv-python==4.5.5.64
```

Try `import cv2`, if you get `ImportError: libGL.so.1: cannot open shared object file: No such file or directory`, run

```
apt-get update
```

```
apt-get install -y python3-opencv
```

`import cv2` should work now. Not sure if this is the right way to work with docker containers, but at least it works for me (?)