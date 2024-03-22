import json
from bs4 import BeautifulSoup
import asyncio



# Создание HTML-разметки страницы с темной темой и улучшенными стилями
html_page = """
<!DOCTYPE html>
<html>
<head>
    <title>Мосбиржа</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            background-color: #333;
            color: #fff;
            margin: 0;
            padding: 0;
        }
        h1 {
            margin-top: 20px;
        }
        table {
            width: 80%;
            margin: 20px auto;
            border-collapse: collapse;
        }
        th, td {
            border: 2px solid #fff;
            padding: 8px;
            text-align: center;
            font-weight: bold;
        }
        th {
            background-color: #555;
        }
        #searchContainer {
            margin-top: 20px;
        }
        #searchInput {
            padding: 8px;
            width: 50%;
            font-size: 16px;
        }
    </style>
</head>
<body>
    <h1>Таблица с фьючерсами</h1>
    <div id="searchContainer">
        <input type="text" id="searchInput" onkeyup="searchTable()" placeholder="Поиск по активам">
    </div>
    <table>
        <tr>
            <th>Актив 1</th>
            <th>Актив 2</th>
            <th>Спред</th>
            <th>Годовая доходность</th>
        </tr>
    </table>
    <script>
        function searchTable() {
            var input = document.getElementById("searchInput");
            var filter = input.value.toUpperCase();
            var table = document.querySelector("table");
            var rows = table.getElementsByTagName("tr");
            for (var i = 1; i < rows.length; i++) {
                var cells = rows[i].getElementsByTagName("td");
                var found = false;
                for (var j = 0; j < cells.length; j++) {
                    var cellValue = cells[j].textContent || cells[j].innerText;
                    if (cellValue.toUpperCase().indexOf(filter) > -1) {
                        found = true;
                        break;
                    }
                }
                if (found) {
                    rows[i].style.display = "";
                } else {
                    rows[i].style.display = "none";
                }
            }
        }
    </script>
</body>
</html>
"""


# Загрузка данных из JSON файла
async def get_html_page(typee):

            
    
    if typee == 'futures_assets':
        with open('mosbirja/data_futures_assets.json', 'r') as file:
            data = json.load(file)
            filename='output_futures_assets.html'
        
    elif typee == 'futures_futures':
        with open('mosbirja/data_futures_futures.json', 'r') as file:
            data = json.load(file)
            filename='output_futures_futures.html'
            
            
    # Создание объекта BeautifulSoup
    soup = BeautifulSoup(html_page, 'html.parser')

    # Находим тег <table> в объекте BeautifulSoup
    table = soup.find('table')

    # Заполнение таблицы данными из JSON
    for row_data in data:
        row = soup.new_tag('tr')
        for key, value in row_data.items():
            if isinstance(value, float):
                value = round(value, 2)
                value = f"{value}%"
            cell = soup.new_tag('td')
            cell.string = str(value)
            row.append(cell)
        table.append(row)

    # Сортировка значений по алфавиту
    values = [td.get_text() for td in table.find_all('td')]
    values.sort()

    # Упорядочиваем строки в таблице на основе отсортированных значений
    for value in values:
        for row in table.find_all('tr'):
            if value in row.get_text():
                table.append(row)
                break

    # Сохранение результатов в HTML файл
    
    with open(filename, 'w') as output_file:
        output_file.write(soup.prettify())
        
        
if __name__ == '__main__':
    asyncio.run(get_html_page())