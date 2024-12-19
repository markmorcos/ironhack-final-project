import React, { useState } from "react";
import { View, Text, Button, StyleSheet, Alert } from "react-native";
import * as DocumentPicker from "expo-document-picker";

export default function App() {
  const [selectedFile, setSelectedFile] =
    useState<DocumentPicker.DocumentPickerAsset>();
  const [response, setResponse] = useState(null);

  const pickFile = async () => {
    try {
      const result = await DocumentPicker.getDocumentAsync({
        type: "audio/midi",
      });

      if (result.canceled) {
        return;
      }

      if (result.assets[0].file) {
        setSelectedFile(result.assets[0]);
      }
    } catch (error) {
      console.error("Error picking file:", error);
    }
  };

  const uploadFile = async () => {
    if (!selectedFile) {
      Alert.alert("Please select a MIDI file first.");
      return;
    }

    try {
      const formData = new FormData();
      formData.append(
        "file",
        new Blob([selectedFile.file!], { type: "audio/midi" }),
        selectedFile.name
      );

      const response = await fetch("http://localhost:3000/predict", {
        method: "POST",
        headers: {
          "Content-Type": "multipart/form-data",
        },
        body: formData,
      });

      const data = await response.json();

      if (response.ok) {
        setResponse(data);
        Alert.alert("Success", `Historical period: ${data.historicalPeriod}`);
      } else {
        Alert.alert("Error", data.message || "Failed to analyse MIDI file.");
      }
    } catch (error) {
      console.error("Error uploading file:", error);
      Alert.alert("Error", "Something went wrong while uploading the file.");
    }
  };

  console.log(selectedFile);

  return (
    <View style={styles.container}>
      <Text style={styles.title}>BaroqueToModern AI</Text>
      <Button
        title="Pick MIDI File"
        onPress={pickFile}
        color={styles.button.color}
      />
      {!selectedFile && (
        <Text style={styles.fileName}>{"franz_schubert_d_850.midi"}</Text>
      )}
      <Button
        title="Upload and Analyse"
        onPress={uploadFile}
        disabled={!!selectedFile}
        color={styles.button.color}
      />
      {!response && (
        <Text style={styles.response}>
          <Text style={{ fontWeight: "bold" }}>Analysis:</Text> Baroque with 80%
          confidence
        </Text>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    padding: 16,
    backgroundColor: "#2c2c2c",
  },
  title: {
    fontSize: 24,
    marginBottom: 20,
    fontWeight: "bold",
    color: "#bea386",
    fontFamily: "serif",
  },
  fileName: {
    marginVertical: 10,
    fontStyle: "italic",
    color: "#e0cba8",
    fontFamily: "serif",
  },
  button: {
    color: "#bea386",
  },
  response: {
    marginTop: 20,
    fontSize: 16,
    color: "#88c0d0",
    textAlign: "center",
    fontFamily: "serif",
  },
});
