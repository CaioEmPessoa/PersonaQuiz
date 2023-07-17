from helpers import perguntas
from helpers import last_user

perguntas = perguntas.Questions()
user_info = last_user.UserInfo()

print("Olá, escolha um nome de usuário para se fazer o quiz.")
username = input(">> ")


user_info.get_user_info(username)
