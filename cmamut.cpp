#include <conio.h>
#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <algorithm>
using std::cout;
using std::cin;
using std::cerr;
using std::endl;
using std::string;
using std::ifstream;
using std::ofstream;
using std::vector;

//from Charles Salvia on stackoverflow.com, ty
bool is_number(const std::string& s){
	return !s.empty() && std::find_if(s.begin(), 
        s.end(), [](unsigned char c) { return !std::isdigit(c); }) == s.end();
}

vector<string> tokens;

string get_code_string(string file_name){
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
	bool literal_string = false;

	for(char c : code){
		if(c == '\t') continue;

		if(c == '"'){
			literal_string = !literal_string;
		}

		if(c == ' '){
			if(!literal_string){
				tokens.push_back(token);
				token = "";
			}else{
				token += ' ';
			}
		}else{
			token += c;
		}
	}
	tokens.push_back(token);
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

int main(){
	string file_name = "";
	cin >> file_name;
	if(file_name == ""){
		return 0;
	}

	string code = get_code_string(file_name+".cmt");
	tokenize(code);
	string final_code = process_code();
	save_asm(file_name+".asm", final_code);
	if(final_code != ""){
		cout << "compilacion exitosa papus Bv";
	}

	getche();
    return 0;
}