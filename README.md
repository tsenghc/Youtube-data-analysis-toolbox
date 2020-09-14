# Youtube-data-analysis-toolbox (Youtube影片數據分析工具)
> Project detail please reference FUTURE.md

## Requirement
* Ubuntu (18.04 or previous version)
* Windows 10
* Python 3.8
## Quick start
This porject using Python virtual enviroment
```=shell script
venv/Script/activate 
```
### Init DB
> Using PGSQL12
```=shell script
python3 service/manage.py db init
```
```=shell script
python3 service/manage.py db migrate
```
```=shell script
python3 service/manage.py db upgrade
```
### API server

```=shell script
python3 service/manage.py runserver
```