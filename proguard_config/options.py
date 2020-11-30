class OptionList(object):
    def __init__(self):
        self.option_list = [
            # Input/Output options
            '-include',
            '-basedirectory',
            '-injars', '-outjars', '-libraryjars',
            '-skipnonpubliclibraryclasses',
            '-dontskipnonpubliclibraryclasses',
            '-dontskipnonpubliclibraryclassmembers',
            '-keepdirectories ',
            '-target',
            '-forceprocessing',
            # Keep options
            '-keep',
            '-keepclassmembers',
            '-keepclasseswithmembers',
            '-keepnames', # -keep,allowshrinking
            '-keepclassmembernames', # -keepclassmembers,allowshrinking
            '-keepclasseswithmembernames' # -keepclasseswithmembers,allowshrinking
            '-if',
            '-printseeds'
            # Shrinking options
            '-dontshrink',
            '-printusage',
            '-whyareyoukeeping',
            # Optimization options
            '-dontoptimize',
            '-optimizations',
            'optimizationpasses',
            '-assumenosideeffects',
            '-assumenoexternalsideeffects',
            '-assumenoescapingparameters',
            '-assumenoexternalreturnvalues',
            '-assumevalues',
            '-allowaccessmodification',
            'mergeinterfacesaggressively',
            # Obfuscation ophtions
            '-dontobfuscate',
            '-printmapping',
            '-applymapping',
            '-obfuscationdictionary',
            '-classobfuscationdictionary',
            '-packageobfuscationdictionary',
            '-overloadaggressively',
            '-useuniqueclassmembernames',
            '-dontusemixedcaseclassnames',
            '-keeppackagenames',
            '-flattenpackagehierarchy',
            '-repackageclasses',
            '-keepattributes',
            '-keepparameternames',
            '-renamesourcefileattribute',
            '-keepkotlinmetadata',
            '-adaptclassstrings',
            '-adaptresourcefilenames',
            '-adaptresourcefilecontents',
            # Preverification options
            '-dontpreverify',
            '-microedition',
            '-android',
            # General options
            '-verbose',
            '-dontnote',
            '-dontwarn',
            '-ignorewarnings',
            '-printconfiguration',
            '-dump',
            '-addconfigurationdebugging'
        ]
        self.keep_option_modifier = [
            'includedescriptorclasses',
            'includecode',
            'allowshrinking',
            'allowoptimization',
            'allowobfuscation'
        ]
        self.optinal_attribute = [
            'SourceFile',
            'SourceDir',
            'InnerClasses',
            'EnclosingMethod',
            'Deprecated',
            'Synthetic',
            'Signature',
            'MethodParameters',
            'Exceptions',
            'LineNumberTable',
            'LocalVariableTable',
            'LocalVariableTypeTable',
            'RuntimeVisibleAnnotations',
            'RuntimeInvisibleAnnotations',
            'RuntimeVisibleParameterAnnotations',
            'RuntimeInvisibleParameterAnnotations',
            'RuntimeVisibleTypeAnnotations',
            'RuntimeInvisibleTypeAnnotations',
            'AnnotationDefault'
        ]

    def get_list(self):
        return self.option_list

    def get_modifier(self):
        return self.keep_option_modifier

    def get_optinal_attribute(self):
        return self.optinal_attribute