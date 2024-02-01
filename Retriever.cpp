#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <chrono>
#include <cstdlib>
#include <sstream>

void splitString(const std::string &str, std::string &DNA_line, std::string &SCORE_line) {
    std::stringstream ss(str);
    std::string word;
    int wordCount = 0;
    while (ss >> word && wordCount < 11) {
        if (wordCount == 9) {
            DNA_line = word;
        } else if (wordCount == 10) {
            SCORE_line = word;
        }
        ++wordCount;
    }
}

void retrieve(const std::string &inputFileName, const std::string &outputFileNameDNA,
              const std::string &outputFileNameQualityScore) {
    auto startTime = std::chrono::high_resolution_clock::now();

    std::ifstream inputFile(inputFileName);
    std::ofstream dnaFile(outputFileNameDNA);
    std::ofstream scoreFile(outputFileNameQualityScore);
    std::string binFileName = outputFileNameQualityScore.substr(0, outputFileNameQualityScore.size() - 4) + "_bin.bin";
    std::ofstream binFile(binFileName, std::ios::binary);

    if (!inputFile) {
        std::cerr << "Error opening input file!" << std::endl;
        return;
    }
    if (!dnaFile) {
        std::cerr << "Error opening DNA output file!" << std::endl;
        return;
    }
    if (!scoreFile) {
        std::cerr << "Error opening score output file!" << std::endl;
        return;
    }
    if (!binFile) {
        std::cerr << "Error opening binary output file!" << std::endl;
        return;
    }

    std::cout << "Files opened successfully." << std::endl;

    const int readBatchSize = 100000;  // Number of lines to read in each batch
    std::string line, batchDNA, batchSCORE;
    int count = 0;
    std::vector<float> buffer;


    while (std::getline(inputFile, line) && count < 5000000) {
        if (line[0] != '@') {
            std::string DNA_Output, SCORE_Output;
            splitString(line, DNA_Output, SCORE_Output);
            if (!DNA_Output.empty() && !SCORE_Output.empty()) {
                batchDNA += DNA_Output;
                batchSCORE += SCORE_Output;

                for (char ch : SCORE_Output) {
                    float f = static_cast<float>(static_cast<int>(ch) - 33);
                    buffer.push_back(f);
                }

                if (++count % readBatchSize == 0) {
                    dnaFile << batchDNA;
                    scoreFile << batchSCORE;
                    binFile.write(reinterpret_cast<const char*>(buffer.data()), buffer.size() * sizeof(float));
                    batchDNA.clear();
                    batchSCORE.clear();
                    buffer.clear();
                }
            }
        }
    }

    if (!batchDNA.empty()) {
        dnaFile << batchDNA;
        scoreFile << batchSCORE;
        binFile.write(reinterpret_cast<const char*>(buffer.data()), buffer.size() * sizeof(float));
    }

    auto elapsedTime = std::chrono::high_resolution_clock::now() - startTime;
    std::cout << "Elapsed time: "
              << std::chrono::duration_cast<std::chrono::seconds>(elapsedTime).count()
              << " seconds" << std::endl;
    std::cout << "DNA content written to " << outputFileNameDNA << std::endl;
    std::cout << "SCORE content written to " << outputFileNameQualityScore << std::endl;
    std::cout << "Binary Score content written to " << binFileName << std::endl;
}

int main(int argc, char *argv[]) {
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
