# A simple version for reproducing quickly

## Environment
```
$ conda create -n libid python=2.7
$ conda activate libid
$ pip install -r requirements.tt
Follow the steps in "https://www.gurobi.com/downloads/end-user-license-agreement-academic/" and get a license
$ conda config --add channels http://conda.anaconda.org/gurobi
$ conda install gurobi
$ pip install PyGithub
$ cd /home/v-xiaody/teamdrive/sciteamdrive2/v-xiaody/LibID
```
## Data
```
Data are downloaded from this repo: https://github.com/presto-osu/orlis-orcis/tree/master/orlis/open_source_benchmarks
and saved at sciteamdrive2/v-xiaody/orlis/. You can use cp to transfer data to sciteamdrive/v-xiaody/LibID/data
```
## Profiling
The following is profile libraries, profile apks(using dasho or allotori obfuscator). The generated profiles will be stored as .json files under profiles_reproduce.
```
$ python LibID.py profile -d data/dasho -p 1 -o profiles/dasho_app
$ python LibID.py profile -d data/allotori -p 1 -o profiles/allotori_app

optional arguments:
  -o FOLDER           specify output folder
  -p N                the number of processes to use [default: the number of CPUs in the system]
  -v                  show debug information
  -d FOLDER           the folder that contains app/library binaries
```

## Detection
The following is libraries-apks(using dasho or allotori) matching. The result is stored under the `outputs_reproduce` folder as a .json file
```
$ python LibID.py detect -ad profiles/dasho_app -ld profiles/lib -p 1 -o outputs/dasho
$ python LibID.py detect -ad profiles/allotori_app / -ld profiles/lib -p 1 -o outputs/allotori

optional arguments:
  -o FOLDER            specify output folder
  -b                   considering build-in Android libraries
  -p N                 the number of processes to use [default: the number of CPUs in the system]
  -A                   run program in Lib-A mode [default: LibID-S mode]
  -r                   consider classes repackaging
  -ad FOLDER           the folder that contains app profiles
  -ld FOLDER           the folder that contains library profiles
```

## Evaluation
```
$ python evaluation.py
```

## JSON format

The result is stored under the `outputs_reproduce` folder as a .json file:
```
$ python -m json.tool outputs/xxxxx.json
```

```
And the result format looks like that:
{
    "appID": "com.example.root.analyticaltranslator",
    "filename": "com.example.root.analyticaltranslator_6.apk",
    "libraries": [
        {
            "category": "example",
            "matched_root_package": [
                "Lcom/squareup/okhttp"
            ],
            "name": "okhttp",
            "root_package_exist": true,
            "shrink_percentage": 1.0,
            "similarity": 1.0,
            "version": [
                "2.3.0"
            ]
        }
    ],
    "permissions": [
        "android.permission.INTERNET"
    ],
    "time": 3.760045051574707
}
```

## Evaluate
```
$ python evaluate.py --reference_dir=outputs/dasho
$ python evaluate.py --reference_dir=outputs/allatori
```