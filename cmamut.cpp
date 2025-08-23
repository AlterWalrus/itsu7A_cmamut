#include <algorithm>
#include <iostream>
#include <fstream>
#include <conio.h>
#include <string>
#include <vector>
using std::cout;
using std::cin;
using std::cerr;
using std::endl;
using std::string;
using std::ifstream;
using std::ofstream;
using std::vector;

bool is_number(const std::string& s){
	return !s.empty() && std::find_if(s.begin(), 
        s.end(), [](unsigned char c) { return !std::isdigit(c); }) == s.end();
}

vector<string> tokens;

string read_file(string file_name){
	ifstream file(file_name);
    if(!file.is_open()){
        cerr << "[ERRROR] Archivo no encontrado :'v" << endl;
        return "";
    }
	string code = "";
	string line;
    while(getline(file, line)){
		line += ' ';
		code += line;
    }
    file.close();
	return code;
}

void save_asm(string file_name, string code){
	if(code == "") return;

	ofstream file(file_name);
    if(file.is_open()){
        file << code;
        file.close();
    }else{
        cout << "[ERROR] Error al guardar codigo generado :'v";
    }
}

void tokenize(string code){
	string token = "";
	bool in_string = false;

	for(char c : code){
		if(isspace(c) && !in_string) {
			if(!token.empty()) {
				tokens.push_back(token);
				token.clear();
			}
		} else if(c == '"') {
			in_string = !in_string;
			token += c;
			if(!in_string) {
				tokens.push_back(token);
				token.clear();
			}
		} else {
			token += c;
		}
	}
}

string process_code(){
	string data = "";
	string code = "";

	for(int i = 0; i < tokens.size(); i++){
		string token = tokens[i];

		//input
		if(token == "plox"){
			token = tokens[++i];
			code += "call read_num\nmov " + token + ", al\n";
		}else

		//Output
		if(token == ":v"){
			token = tokens[++i];
			if(token[0] == '"'){
				token = token.substr(1, token.length()-2);
				data += "s" + std::to_string(i) + " db '" + token + "', 10, '$'\n";
				code += "print s" + std::to_string(i) + "\n";
			}else{
				code += "mov al, " + token + "\ncall print_num\n";
			}
		}else

		//Variables
		if(token == "var"){
			token = tokens[++i];
			data += token + " db ?\n";
		}else

		//Values
		if(token == "="){
			string var_name = tokens[i-1];
			
			//Math (ew...)
			if(tokens[i+2] == "+"){
				code += "mov al, " + tokens[i+1] + "\nadd al, " + tokens[i+3] + "\nmov " + var_name + ", al\n";
			}else
			if(tokens[i+2] == "-"){
				code += "mov al, " + tokens[i+1] + "\nsub al, " + tokens[i+3] + "\nmov " + var_name + ", al\n";
			}else{
				//No math (yey!)
				token = tokens[++i];
				if(is_number(token)){
					code += "mov " + var_name + ", " + token + "\n";
				}else{
					code += "mov al, " + token + "\nmov " + var_name + ", al\n";
				}
			}
		}
	}

	if(data == "" && code == ""){
		return "";
	}

	string final_code = "";
	ifstream file("template.asm");
    if(!file.is_open()){
        cerr << "[ERRROR] Archivo base ASM no encontrado :'v" << endl;
        return "";
    }
	string line;
    while(getline(file, line)){
		if(line == ";DATABLOCK"){
			final_code += data;
		}else
		if(line == ";CODEBLOCK"){
			final_code += code;
		}else{
			line += '\n';
			final_code += line;
		}
    }
    file.close();
	return final_code;
}

bool compile(string file_name){
	string code = read_file(file_name+".cmt");
	if(code.empty()) return false;
	
	tokenize(code);
	string final_code = process_code();
	save_asm(file_name+".asm", final_code);
}

int main(){
	string file_name = "";
	cin >> file_name;
	
	if(compile(file_name)){
		cout << "compilacion exitosa papus Bv";
	}

	getche();
    return 0;
}