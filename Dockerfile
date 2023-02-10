FROM holdenk/rayray:nightly
# On ARM we _sometimes_ need to build the PostGres connector from source (depending on version).
RUN sudo apt-get update && sudo apt-get upgrade -y && sudo apt-get install -y libpq-dev
# Setup the dependencies in advance
COPY requirements.txt /tmp/req.txt
# See https://github.com/python/typing/issues/573
RUN pip uninstall -y typing
RUN pip install -U -r /tmp/req.txt
COPY backend/pcf-web/src/requirements/*.txt /tmp/
RUN pip install -U -r /tmp/local.txt
RUN sudo mkdir -p /apps/backend; sudo chown -R ray /apps
COPY ./backend /apps/backend
COPY ./setup.py /apps
RUN cd /apps; pip install -e .; cd -
