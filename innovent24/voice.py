import azure.cognitiveservices.speech as speechsdk

# Azure Speech Service subscription details
subscription_key = "1GiDM8kscBYkntG4w9sK4rRd5AbfYXSBeyEDEsDrvhr8CZaXeI17JQQJ99AKACYeBjFXJ3w3AAAYACOGBHLr"
region = "eastus"


def translate_speech_to_english():
    # Initialize the Speech Translation Config
    translation_config = speechsdk.translation.SpeechTranslationConfig(
        subscription=subscription_key,
        region=region
    )

    # Enable automatic language detection
    auto_detect_source_language_config = speechsdk.languageconfig.AutoDetectSourceLanguageConfig(
        languages=["hi-IN", "te-IN", "ta-IN", "de-DE", "en-US"]
        # Supported source languages: Hindi, Telugu, Tamil, German, English
    )

    translation_config.add_target_language("en")  # English as the target language

    # Create a translation recognizer with auto language detection
    recognizer = speechsdk.translation.TranslationRecognizer(
        translation_config=translation_config,
        auto_detect_source_language_config=auto_detect_source_language_config
    )

    print("Speak into the microphone...")

    # Start recognition and translation
    result = recognizer.recognize_once()

    # Handle the result
    if result.reason == speechsdk.ResultReason.TranslatedSpeech:
        detected_language = result.properties[
            speechsdk.PropertyId.SpeechServiceConnection_AutoDetectSourceLanguageResult]
        print(f"Detected Language: {detected_language}")
        print(f"Recognized: {result.text}")
        print(f"Translated to English: {result.translations['en']}")
    elif result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized.")
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print(f"Speech Recognition canceled: {cancellation_details.reason}")
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print(f"Error details: {cancellation_details.error_details}")


# Run the translation
translate_speech_to_english()
