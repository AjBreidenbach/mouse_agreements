FROM ubuntu
workdir /root
RUN apt-get update --fix-missing
RUN apt-get install -y \
  pandoc \
  python3-pip \
  python3-venv \
  libssl-dev \
  curl \
  git

COPY Pipfile ./

RUN sed -i "s/3\.9/3\.8\.5/" Pipfile

RUN python3 -m pip install --user pipx
RUN python3 -m pipx ensurepath
RUN python3 -m pipx install pipenv
RUN curl https://pyenv.run | bash
RUN ln -s /bin/bash ./
RUN echo 'eval "$(pyenv init -)"' >> ~/.bashrc
RUN echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc
ENV PATH="/root/.pyenv/bin:$PATH"
RUN echo "echo Y | pipenv install --python 3.8.5" | bash --login 

COPY *.py run.sh .env ./
COPY static ./static/

CMD ["bash", "--login", "run.sh"]
