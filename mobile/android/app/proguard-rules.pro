# ============================================================

# MAIN BASE FOUNDATION — ANDROID RELEASE RULES

# ============================================================

# Keep Android Activity classes

-keep public class * extends android.app.Activity {
public <init>();
}

# Keep Application classes

-keep public class * extends android.app.Application {
public <init>();
}

# Keep Parcelable implementations

-keep class * implements android.os.Parcelable {
public static ** CREATOR;
}

# Keep Serializable classes

-keepclassmembers class * implements java.io.Serializable {
static final long serialVersionUID;
private static final java.io.ObjectStreamField[] serialPersistentFields;
private void writeObject(java.io.ObjectOutputStream);
private void readObject(java.io.ObjectInputStream);
}

# Keep WebView JavaScript interfaces

-keepclassmembers class * {
@android.webkit.JavascriptInterface <methods>;
}

# Keep annotation metadata

-keepattributes *Annotation*
-keepattributes Signature
-keepattributes InnerClasses
-keepattributes EnclosingMethod

# Do not expose debug information in release builds

-renamesourcefileattribute SourceFile
-keepattributes SourceFile,LineNumberTable

# ============================================================

# END

# ============================================================
