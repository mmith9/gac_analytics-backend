import uvicorn
import logging
import logging.config
logging.config.fileConfig("logging.conf")
logger = logging.getLogger(__name__)
from pprint import PrettyPrinter

pp=PrettyPrinter()


#log_config = uvicorn.config.LOGGING_CONFIG
#pp.pprint(log_config)

#logging.config.dictConfig(log_config)
#log_config["formatters"]["access"]["fmt"] = "%(asctime)s - %(levelname)s - %(message)s"
#log_config["formatters"]["default"]["fmt"] = "%(asctime)s - %(levelname)s - %(message)s"
#log_config['loggers']['uvicorn.access']['propagate'] = True

if __name__ == "__main__":
    uvicorn.run("app.api:app", host="0.0.0.0", port=8000, reload=True,
                reload_dirs="./app/", reload_delay=2) #, log_config=log_config)  # , log_level='trace')
    