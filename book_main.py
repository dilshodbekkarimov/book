
import logging
from aiogram.dispatcher.filters import Text
from aiogram import Bot, Dispatcher, executor, types
from book_baza import * 
from book_button import *
from book_tokenn import *

logging.basicConfig(level=logging.INFO)


bot = Bot(token=API_TOKEN)

###########################################################################################################################################################










from aiogram.contrib.fsm_storage.memory import  MemoryStorage # vaqtinchalik xotra uchun 
from aiogram.dispatcher import FSMContext #state uchun 
from book_state import StateData



dp = Dispatcher(bot, storage=MemoryStorage())#vaqtinchalik xotira
db = Database()


db.create_category()
db.create_table_products()



@dp.message_handler(commands="book_add", state="*",user_id=admin)
async def send_welcome(message: types.Message,  state: FSMContext):
    await message.answer("Kitobning nomini kiriting:")
    await state.set_state(StateData.name)
   


@dp.message_handler(state=StateData.name)
async def echo(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        await message.answer("kitobning nomini matin ko'rinishida kiriting")
        return
    await state.update_data(name=message.text)
    await message.answer("category idsini kiriting: ")
    await StateData.next()

@dp.message_handler(state=StateData.category_id)
async def echo(message: types.Message, state: FSMContext):
    if message.text.isalpha():
        await message.answer("category idisini raqam ko'rinishida kiriting")
        return
    await state.update_data(category_id=message.text)
    await message.answer("kitobga tarif bering: ")
    await StateData.next()
    
@dp.message_handler(state=StateData.description)
async def echo(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer("kitobning muallifini kiriting: ")
    await StateData.next()




@dp.message_handler(state=StateData.muallif)
async def echo(message: types.Message, state: FSMContext):
    await state.update_data(muallif=message.text)
    await message.answer("kitob chiqqan yilini kiriting ")
    await StateData.next()


@dp.message_handler(state=StateData.yili)
async def echo(message: types.Message, state: FSMContext):
    await state.update_data(yili=message.text)
    await message.answer("kitobni /file/  yuboring: ")
    await StateData.next()



@dp.message_handler(content_types='any', state=StateData.book)
async def echo(message: types.Message, state: FSMContext):
    if message.content_type != "document":
        await message.answer("kitoblarni fayl ko'rinishida joylang")
        return
  
    await state.update_data(book=message.document['file_id'])
    await message.answer("kitobning rasimini  kiriting")
    await StateData.next()
   



@dp.message_handler(content_types="any", state=StateData.photo)
async def echo(message: types.Message, state: FSMContext):
    if message.content_type != "photo":
        await message.answer("rasimni jpg farmatda kiriting")
        return
    await state.update_data(photo=message.photo[-1]['file_id'])
    data = await state.get_data()
    name_ = data.get("name")
    category_id_ = data.get("category_id")
    description_ = data.get("description")
    muallif_ = data.get("muallif")
    yili_ = data.get("yili")
    book_ = data.get("book")
    photo_ = data.get("photo")

    db.insert_products(name_,category_id_,description_,muallif_,yili_,book_,photo_)



    await state.finish()
    await state.reset_state()
    await message.answer("Ma'lumotlar saqlandi!!!")
    # print(name_,description_,muallif_,yili_,photo_,book_,category_id_)
    await message.answer_photo(photo=photo_,caption=f"📚Kitobning nomi: {name_},\n\n✅Kitobingiz category idsi {category_id_}\n\n📖Kitobga qisqacha tarif: {description_},\n\n🔖Kitob {yili_}-yili chiqqan,\n\n📝Kitobning muallifi: {muallif_}")
    await message.answer_document(document=book_)








############################################################################################################################################################################################

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("👋Assalomu alaykum\n\n✅Xo'sh kelibsiz",reply_markup=menu)

@dp.message_handler(text='📚Kitoblar')
async def send_welcome(message: types.Message):
    markup = await for_catefory_get_all()
    await message.reply("✅bo'limlardan birini tanlang: ",reply_markup=markup)

@dp.callback_query_handler(Text(startswith="productall_"))
async def send_welcome(call: types.CallbackQuery):
    index = call.data.index("_")
    id = call.data[index+1:]
    products = await get_category_id(id)
    # print('salom',products)
    await call.message.reply("📚kitoblardan birini tanlang!!!",reply_markup=products)




@dp.callback_query_handler(Text(startswith="products_"))
async def send_welcome(call: types.CallbackQuery):
    index = call.data.index("_")
    id = call.data[index+1:]
    product = db.select_product_id(id)
    # print(product)
    await call.message.answer_photo(photo=product[7],caption=f"📚Kitobning nomi: {product[2]},\n\n\n✅Kitobga qisqacha tarif: {product[3]},\n\n✅Kitob {product[5]}-yili chiqqan,\n\n📝Kitobning muallifi: {product[4]}")
    await call.message.answer_document(document=product[6])



####################################
#####################################################################################################################################################################################################################################
#####################################

@dp.message_handler(text='🔍Qidirish')
async def send_welcome(message: types.Message):
    await message.reply("⏳Ushbu qism hozirda sozlanmoqda,\n\n✅Biz bilan qolganingiz uchun minnatdormiz!!!")

@dp.message_handler(text='☎️Aloqa')
async def send_welcome(message: types.Message):
    await message.reply("✅Assalomu alaykum hurmatli foydalanuvchi!!!\n\n✅Takliflaringizni quydagi botga yozib qoldiring: @Bot_botda_bu_bot \n\n✅Bizni tanlaganingiz uchun rahmat!!!")





if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)