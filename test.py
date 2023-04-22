if os.path.exists(f'allcases/{message.from_user.id}/{message.from_user.id}.txt'):
    data, msg = [], '<b>Ваш портфель:</b>\n\n'
    with open(f'allcases/{message.from_user.id}/{message.from_user.id}.txt', 'r') as f:
        tmp = f.readlines()

        for i in tmp:
            i = i.replace('\n', '')
            data.append(list(i.split(' ')))
    for i in data:
        msg += f'<b>{i[0]}</b> - ${i[1]}<i>({i[2]})</i>\n'

    await bot.send_message(message.from_user.id, '<b>Инструкция:</b>\n\n<code>/case create</code> - создать новый портфель\n<code>/case update</code> - добавить новые монеты\n<code>/case clear</code> - удалить портфель\n\n<i>Нажмите, чтобы скопировать.</i>')
    await bot.send_message(message.from_user.id, msg)
else:
    await bot.send_message(message.from_user.id, '<b>Портфель еще не создан!</b>\n\n<b>Введите:</b> <code>/case create</code>\n<i>Нажмите, чтобы скопировать.</i>')
