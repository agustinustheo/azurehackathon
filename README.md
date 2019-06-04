# JudgeYou
An app made for Azure Hackathon

## Installation
### Linux
This is tested on Ubuntu. Please refer to OpenCV docs for other linux distros
- Create virtual env name judgeyou  
  <b><i>important!: you must name the env judgeyou if you use linux-installation.sh</i></b>
    ```
    # --- Install python3 dev
    sudo apt-get install python3-dev

    # --- install virtualenv and virtualenvwrapper
    wget https://bootstrap.pypa.io/get-pip.py
    sudo python3 get-pip.py
    sudo pip install virtualenv virtualenvwrapper
    sudo rm -rf ~/get-pip.py ~/.cache/pip

    echo -e "\n# virtualenv and virtualenvwrapper" >> ~/.bashrc
    echo "export WORKON_HOME=$HOME/.virtualenvs" >> ~/.bashrc
    echo "export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3" >> ~/.bashrc
    echo "source /usr/local/bin/virtualenvwrapper.sh" >> ~/.bashrc

    source ~/.bashrc

    # ------ create virtual environment judgeyou ----
    mkvirtualenv judgeyou -p python3
    workon judgeyou
    ```

- Make linux-installation.sh executable
    ```
    sudo chmod +x linux-installation.sh
    ```

- Run linux-installation.sh
    ```
    ./linux-installation.sh
    ```
    This will download opencv and opencv_contrib repositories at home directory.  
    It will then build and install opencv at /usr/local/lib/python3.6/site-packages.  
    It will use judgeyou virtual env's python interpreter

- Link installed opencv to judgeyou environment
    ```
    # --- link opencv to judgeyou virtual env ---
    workon judgeyou
    cd ~/.virtualenvs/judgeyou/lib/python3.6/site-packages/
    ln -s /usr/local/lib/python3.6/site-packages/cv2/python-3.6/cv2.cpython-36m-x86_64-linux-gnu.so cv2.so
    ```

- Check if cv2 is installed
    ```
    $ python
    $ >>> import cv2
    $ >>> cv2.__version__
    ```

- Install requirements-linux.txt
    ```
    pip install -r requirements-linux.txt
    ```