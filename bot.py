import vk_api, random, time
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

bot_group = *bot_group_id*
peer_offset = 2000000000
nums = list(range(1,2))
tried = set()
end = False

def send_chat(peer, msg):
	vk.messages.send(peer_id=peer, group_id=bot_group, random_id=random.randint(-9223372036854775808,9223372036854775807), message=msg)

def get_admins(peer):
	admins = []
	users = vk.messages.getConversationMembers(peer_id=peer, group_id=bot_group)['items']
	for user in users:
		if user.get('is_admin'):
			admins.append(user['member_id'])
	
	return admins

vk_session = vk_api.VkApi(token='*group_token*')
vk = vk_session.get_api()

longpoll = VkBotLongPoll(vk=vk_session,group_id=bot_group,wait=25)

print('Бот запущен.')


for event in longpoll.listen():
	try:
		message = event.object['message']
		if 'text' in message and VkBotEventType.MESSAGE_NEW:
			if event.from_user and message['out'] == 0:
				id = message['from_id']
				msg_text = message['text']
				
				continue
				
			if event.from_chat:
				id = message['from_id']
				msg_text = message['text'].lower()
				from_peer = message['peer_id']
				
				admins = get_admins(from_peer)
				if msg_text[:5] == 'бот, ':
					msg_text = msg_text.lower()[5:]
					
					if (msg_text == 'начать'):
						send_chat(from_peer, 'Привет, я бот Санта.\nСегодня, я помогу вам узнать того, кому вы будете дарить подарок или настроение.\nДля этого, я выдам вам число после того, как вы напишите:\nБот, рандом')
						continue
					
					if (msg_text == 'сброс'):
						if id in admins:
							nums = list(range(1,17))
							tried = set()
							end = False
							send_chat(from_peer, 'Сброшено 👌')
						else:
							send_chat(from_peer, 'Сброс могут делать только администраторы ⛔')
						continue
						
					if (msg_text == 'конец' and not end):
						if id in admins:
							end = True
							nums = []
							tried = set()
							send_chat(from_peer, '⎯⎯⎯⎯⎯🎄🎁⛔⎯⎯⎯⎯⎯\nА теперь ждите билетик!')
						else:
							send_chat(from_peer, 'Заканчивать могут только администраторы ⛔')
						continue
					
					if (msg_text == 'рандом'):
						c = len(nums)
						if (c > 0):
							if not id in tried:
								tried.add(id)
								i = random.randint(0, c-1)
								num = nums.pop(i)
								send_chat(from_peer, str(num) + ' 🎁')
							else:
								send_chat(from_peer, 'Вы уже пробовали! ⚠')
						else:
							send_chat(from_peer, '⎯⎯⎯⎯⎯🎄🎁⛔⎯⎯⎯⎯⎯')
	except Exception as e:
		send_chat(from_peer, 'Ошибка')
		print(f'Exception: {e}')