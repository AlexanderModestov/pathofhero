


@router.message(CommandStart())
async def cmd_start(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.button(text="Заполнить профиль", callback_data="profile")
    markup = InlineKeyboardMarkup(inline_keyboard=builder.export())
    await message.answer(text=first_step, reply_markup=markup)
    db_worker.create_profile(user_id=message.from_user.id)
    await message.delete()

@router.message(Command('about'))
async def cmd_start(message: types.Message):
    text = '''Мир меняется в социальном, экономическом, геополитическом, климатическом и технологическом плане... слишком быстро. Старые глобальные системы рушатся одна за другой или все одновременно.\n\nМиллионы людей сталкиваются с изменением условий жизни,  вынуждены иммигрировать и строить новую жизнь. \n\nЛюди нуждаются в помощи, чтобы адаптироваться к новым условиям, понять свою уникальность и позиционировать себя в новом рынке, стране и обществе. \n\nUnuquer.us – это инструмент, чтобы поддержать каждого с помощью проверенного веками метода архетипов и новейших AI-технологий, которые мы будем внедрять по мере развития проекта. На первом этапе пользователи узнают себя лучше и поймут свою уникальность, на втором – с помощью AI создадут персональные носители информации, чтобы  позиционировать себя и эффективно вести коммуникации. На третьем – появиться P2P биржа вакансий и обмена опытом, личной и профессиональной уникальностью.'''
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(InlineKeyboardButton('Интересно, хочу попробовать!'), InlineKeyboardButton('Ничего не понятно'), InlineKeyboardButton('Понятно, не интересно'))
    send_message = await message.answer(text=text, reply_markup=markup)
    await message.delete()

@router.message(Command('feedback'))
async def cmd_start(message: types.Message):
    text = '''В конструктивной форме будем рады любой критике, предложениям, идеям!\n
    Благодарим за твой вклад! Можем связаться, если захотим уточнить что-то?'''
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(InlineKeyboardButton('Да'), InlineKeyboardButton('Нет'))
    await message.answer(text=text, reply_markup=markup)
    await message.delete()