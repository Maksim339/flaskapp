apt update
su
apt-get install sudo
sudo apt install vim -y
sudo apt install curl -y
apt install unzip -y
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install --update
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
<<EOF
A
EOF
sudo ./aws/install --update
aws --version
aws configure <<EOF
AKIAZ3ZSATRHS3JRM5NZ
EqeJ0GftzSyp0nKnpDA67FI9S1D6BbOResZN1bWe
eu-central-1
json
EOF
