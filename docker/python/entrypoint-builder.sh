#!/usr/bin/env bash

if [ ! ${SKIP_BUILD:-0} -eq 1 ]; then
    echo "Welcome to ${PROJECT_NAME} - backend"
    echo "Building..."

    # using virtualenv to make vendor volumes simpler
    virtualenv --no-site-packages ${PROJECT_VENDOR_DIR}
    source ${PROJECT_VENDOR_DIR}/bin/activate

    pip install --upgrade -r ${BASE_DIR}/docker/python/requirements.txt
    python ${PROJECT_DIR}/manage.py migrate --noinput
    python ${PROJECT_DIR}/manage.py collectstatic --noinput
    echo "Build finished."
fi