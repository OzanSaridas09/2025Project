import sqlite3
import os

def seed():
    # Ensure the instance folder exists for the database
    if not os.path.exists('instance'):
        os.makedirs('instance')

    conn = sqlite3.connect('instance/names.db')
    
    # All 200 names combined
    names_list = [
        "Sean", "Saoirse", "Siobhan", "Aoife", "Niamh", "Cillian", "Eoghan", "Fionn", "Cian", "Daithi", 
        "Aisling", "Orlaith", "Tadhg", "Roisin", "Padraig", "Xochitl", "Joaquin", "Itzel", "Citlali", "Yaretzi", 
        "Ixchel", "Quetzalli", "Cuauhtemoc", "Nguyen", "Phuong", "Quynh", "Thao", "Huy", "Minh", "Tuan", 
        "Trinh", "Bich", "Svetlana", "Anastasiya", "Yevgeniy", "Oleksandr", "Mykhailo", "Bohdan", "Dmytro", "Zoryana", 
        "Kateryna", "Sviatoslav", "Bjorn", "Soren", "Aksel", "Freja", "Stig", "Mikkel", "Jorgen", "Kjell", 
        "Siavash", "Kaveh", "Mehrdad", "Parisa", "Shahrzad", "Khosrow", "Behzad", "Ardeshir", "Farshad", "Pouya", 
        "Roxana", "Sohrab", "Bahram", "Dariush", "Jamshid", "Shahin", "Niloofar", "Golshifteh", "Ramin", "Navid", 
        "Chukwuemeka", "Oluwadamilola", "Babajide", "Adebola", "Funke", "Ayodele", "Yakubu", "Szymon", "Grzegorz", "Wojciech", 
        "Zbigniew", "Czeslaw", "Radoslaw", "Bartosz", "Krzysztof", "Malwina", "Ioannis", "Dimitrios", "Georgios", "Efthymios", 
        "Christos", "Panagiotis", "Nikolaos", "Tsz-Yin", "Cheuk-Man", "Ngai", "Ka-Ming", "Wing-Sze", "Yiu-Chung", "Giuseppe", 
        "Guglielmo", "Alessandro", "Francesca", "Giorgio", "Lorenzo", "Benedetta", "Emanuele", "Guillaume", "Benoit", "Aurelien", 
        "Thierry", "Mathieu", "Francois", "Cecile", "Hrvoje", "Zeljko", "Bojan", "Srdjan", "Vjekoslav", "Eowyn", 
        "Eira", "Isolde", "Sigrid", "Astrid", "Solveig", "Neriah", "Tzofiya", "Avichai", "Shira", "Yehuda", 
        "Eliyahu", "Zhiyuan", "Xiaojing", "Qinghua", "Yuxuan", "Zhihao", "Xinyi", "Qianyu", "Hyun-woo", "Seong-min", 
        "Jae-hyun", "Eun-ji", "Hye-jin", "Yaroslav", "Vladyslav", "Stanislaw", "Miroslav", "Bronislaw",
        "Caoimhe", "Eilidh", "Ruaidhri", "Muireann", "Blathnaid", "Hrafn", "Gudrun", "Eirikr", "Thordis", "Snaebjorn", 
        "Kazimierz", "Przemyslaw", "Wladyslaw", "Slawomir", "Boguslaw", "Yuliana", "Lyubomir", "Dobroslav", "Radomir", "Velimir", 
        "Chinedum", "Nkiru", "Ifeanyichukwu", "Obinna", "Uchechukwu", "Nahuel", "Lautaro", "Yamila", "Milagros", "Soledad", 
        "Ryosuke", "Shunsuke", "Takahiro", "Kazuyoshi", "Yukihiro", "Xiangyu", "Zhixuan", "Qiming", "Xuefeng", "Chunhua", 
        "Sukhdeep", "Harpreet", "Parminder", "Balwinder", "Navjot", "Vasiliy", "Fyodor", "Aleksey", "Yekaterina", "Nadezhda", 
        "Zlatko", "Tomislav", "Dragomir", "Radovan", "Milojko"
    ]

    # Clean existing data to avoid duplicates
    conn.execute("DELETE FROM names")
    
    # Insert the names (is_favorite defaults to 0)
    for name in names_list:
        conn.execute("INSERT INTO names (name, is_favorite) VALUES (?, 0)", (name,))
    
    conn.commit()
    conn.close()
    print(f"Success! {len(names_list)} names are now in your database.")

if __name__ == "__main__":
    seed()