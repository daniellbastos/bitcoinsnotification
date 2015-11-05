#! /bin/bash
source $OPENSHIFT_HOMEDIR/python/virtenv/venv/bin/activate
python $OPENSHIFT_REPO_DIR/cron_update.py
