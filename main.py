from okmcko import get_response
from data_parsing import get_data
from data_filter import filter_new_files
from downloader import download_files

if __name__ == '__main__':

    #TODO теперь, когда мы все получили. Нужна функция со сверкой имеющейся data. Если data.json нет, то создать.
    #TODO а main должен скачать файлы, вернуть список того, что можно отдавать боту и вместо href - пути к файлам и дополнить data.json
    #TODO ещё можно из okmcko убрать все, что связано с токеном мос.ру. В мос.ру из окмцко засунуть проверку токена, загрузку токена и сохранение токена.

    #TODO new нет смысла менять href на путь файла, когда путь и так известен.


    #token = load_token()
    #if is_token_expire():
        #token = get_token()
        #save_token(token)
    response, session = get_response()
    data = get_data(response)
    new_data = filter_new_files(data)
    if new_data:
        download_files(session, new_data)
    else:
        return None
    
    
    
