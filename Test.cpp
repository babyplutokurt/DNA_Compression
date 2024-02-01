#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <chrono>
#include <cstdlib>
#include <sstream>

std::vector<std::string> splitString(const std::string& str) {
    std::stringstream ss(str);
    std::string word;
    std::vector<std::string> words;
    while (ss >> word && word.size() <= 12) {
        words.push_back(word);
    }

    return words;
}

void retrieve(const std::string& inputFileName, const std::string& outputFileNameDNA,
              const std::string& outputFileNameQualityScore) {
    auto startTime = std::chrono::high_resolution_clock::now();

    std::ifstream inputFile(inputFileName);
    std::ofstream dnaFile(outputFileNameDNA);
    std::ofstream scoreFile(outputFileNameQualityScore);
    std::string binFileName = outputFileNameQualityScore.substr(0, outputFileNameQualityScore.size() - 4) + "_bin.bin";
    std::ofstream binFile(binFileName, std::ios::binary);

    if (!inputFile || !dnaFile || !scoreFile || !binFile) {
        std::cerr << "Error opening files!" << std::endl;
        return;
    }

    std::string line;
    int count = 0;
    while (std::getline(inputFile, line)) {
        if (line[0] != '@') {
            count++;
            if (count > 500000) {
                break;
            }
            auto words = splitString(line);
            if (words.size() < 11) {
                continue; // Skip lines with insufficient data
            }
            std::string DNA_Output = words[9];
            std::string SCORE_Output = words[10];

            dnaFile << DNA_Output;
            scoreFile << SCORE_Output;
            for (auto ch : SCORE_Output) {
                float f = static_cast<float>(static_cast<int>(ch) - 33);
                binFile.write(reinterpret_cast<const char*>(&f), sizeof(f));
            }
        }
    }

    auto elapsedTime = std::chrono::high_resolution_clock::now() - startTime;
    std::cout << "Elapsed time: "
              << std::chrono::duration_cast<std::chrono::seconds>(elapsedTime).count()
              << " seconds" << std::endl;
    std::cout << "DNA content written to " << outputFileNameDNA << std::endl;
    std::cout << "SCORE content written to " << outputFileNameQualityScore << std::endl;
    std::cout << "Binary Score content written to " << binFileName << std::endl;
}

int main(int argc, char* argv[]) {
    if (argc != 4) {
        std::cout << "Usage: ./program_name input_file output_file_name_DNA output_file_name_qualityScore" << std::endl;
        return 1;
    }

    std::string inputFileName = argv[1];
    std::string outputFileNameDNA = argv[2];
    std::string outputFileNameQualityScore = argv[3];
    retrieve(inputFileName, outputFileNameDNA, outputFileNameQualityScore);

    return 0;
}