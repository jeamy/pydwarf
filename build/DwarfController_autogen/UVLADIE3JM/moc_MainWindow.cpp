/****************************************************************************
** Meta object code from reading C++ file 'MainWindow.h'
**
** Created by: The Qt Meta Object Compiler version 69 (Qt 6.10.1)
**
** WARNING! All changes made in this file will be lost!
*****************************************************************************/

#include "../../../src/MainWindow.h"
#include <QtNetwork/QSslError>
#include <QtGui/qtextcursor.h>
#include <QtCore/qmetatype.h>

#include <QtCore/qtmochelpers.h>

#include <memory>


#include <QtCore/qxptype_traits.h>
#if !defined(Q_MOC_OUTPUT_REVISION)
#error "The header file 'MainWindow.h' doesn't include <QObject>."
#elif Q_MOC_OUTPUT_REVISION != 69
#error "This file was generated using the moc from 6.10.1. It"
#error "cannot be used with the include files from this version of Qt."
#error "(The moc has changed too much.)"
#endif

#ifndef Q_CONSTINIT
#define Q_CONSTINIT
#endif

QT_WARNING_PUSH
QT_WARNING_DISABLE_DEPRECATED
QT_WARNING_DISABLE_GCC("-Wuseless-cast")
namespace {
struct qt_meta_tag_ZN14ClickableLabelE_t {};
} // unnamed namespace

template <> constexpr inline auto ClickableLabel::qt_create_metaobjectdata<qt_meta_tag_ZN14ClickableLabelE_t>()
{
    namespace QMC = QtMocConstants;
    QtMocHelpers::StringRefStorage qt_stringData {
        "ClickableLabel",
        "clicked",
        ""
    };

    QtMocHelpers::UintData qt_methods {
        // Signal 'clicked'
        QtMocHelpers::SignalData<void()>(1, 2, QMC::AccessPublic, QMetaType::Void),
    };
    QtMocHelpers::UintData qt_properties {
    };
    QtMocHelpers::UintData qt_enums {
    };
    return QtMocHelpers::metaObjectData<ClickableLabel, qt_meta_tag_ZN14ClickableLabelE_t>(QMC::MetaObjectFlag{}, qt_stringData,
            qt_methods, qt_properties, qt_enums);
}
Q_CONSTINIT const QMetaObject ClickableLabel::staticMetaObject = { {
    QMetaObject::SuperData::link<QLabel::staticMetaObject>(),
    qt_staticMetaObjectStaticContent<qt_meta_tag_ZN14ClickableLabelE_t>.stringdata,
    qt_staticMetaObjectStaticContent<qt_meta_tag_ZN14ClickableLabelE_t>.data,
    qt_static_metacall,
    nullptr,
    qt_staticMetaObjectRelocatingContent<qt_meta_tag_ZN14ClickableLabelE_t>.metaTypes,
    nullptr
} };

void ClickableLabel::qt_static_metacall(QObject *_o, QMetaObject::Call _c, int _id, void **_a)
{
    auto *_t = static_cast<ClickableLabel *>(_o);
    if (_c == QMetaObject::InvokeMetaMethod) {
        switch (_id) {
        case 0: _t->clicked(); break;
        default: ;
        }
    }
    if (_c == QMetaObject::IndexOfMethod) {
        if (QtMocHelpers::indexOfMethod<void (ClickableLabel::*)()>(_a, &ClickableLabel::clicked, 0))
            return;
    }
}

const QMetaObject *ClickableLabel::metaObject() const
{
    return QObject::d_ptr->metaObject ? QObject::d_ptr->dynamicMetaObject() : &staticMetaObject;
}

void *ClickableLabel::qt_metacast(const char *_clname)
{
    if (!_clname) return nullptr;
    if (!strcmp(_clname, qt_staticMetaObjectStaticContent<qt_meta_tag_ZN14ClickableLabelE_t>.strings))
        return static_cast<void*>(this);
    return QLabel::qt_metacast(_clname);
}

int ClickableLabel::qt_metacall(QMetaObject::Call _c, int _id, void **_a)
{
    _id = QLabel::qt_metacall(_c, _id, _a);
    if (_id < 0)
        return _id;
    if (_c == QMetaObject::InvokeMetaMethod) {
        if (_id < 1)
            qt_static_metacall(this, _c, _id, _a);
        _id -= 1;
    }
    if (_c == QMetaObject::RegisterMethodArgumentMetaType) {
        if (_id < 1)
            *reinterpret_cast<QMetaType *>(_a[0]) = QMetaType();
        _id -= 1;
    }
    return _id;
}

// SIGNAL 0
void ClickableLabel::clicked()
{
    QMetaObject::activate(this, &staticMetaObject, 0, nullptr);
}
namespace {
struct qt_meta_tag_ZN10MainWindowE_t {};
} // unnamed namespace

template <> constexpr inline auto MainWindow::qt_create_metaobjectdata<qt_meta_tag_ZN10MainWindowE_t>()
{
    namespace QMC = QtMocConstants;
    QtMocHelpers::StringRefStorage qt_stringData {
        "MainWindow",
        "onConnectClicked",
        "",
        "onCancelConnectClicked",
        "onScanClicked",
        "onCancelScanClicked",
        "onSubnetTextChanged",
        "text",
        "onWebSocketConnected",
        "onWebSocketDisconnected",
        "onWebSocketError",
        "error",
        "onDeviceFound",
        "DwarfDeviceInfo",
        "info",
        "onScanFinished",
        "onScanProgress",
        "percent",
        "onDeviceSelected",
        "QListWidgetItem*",
        "item",
        "onPipStreamClicked",
        "onCameraSourceTele",
        "onCameraSourceWide",
        "onCameraPhotoClicked",
        "onCameraRecClicked",
        "onExposureModeChanged",
        "index",
        "onShutterSliderChanged",
        "value",
        "onGainSliderChanged",
        "onIrCutToggled",
        "checked",
        "onBinningChanged",
        "onContrastSliderChanged",
        "onSaturationSliderChanged",
        "onSharpnessSliderChanged",
        "onHueSliderChanged"
    };

    QtMocHelpers::UintData qt_methods {
        // Slot 'onConnectClicked'
        QtMocHelpers::SlotData<void()>(1, 2, QMC::AccessPrivate, QMetaType::Void),
        // Slot 'onCancelConnectClicked'
        QtMocHelpers::SlotData<void()>(3, 2, QMC::AccessPrivate, QMetaType::Void),
        // Slot 'onScanClicked'
        QtMocHelpers::SlotData<void()>(4, 2, QMC::AccessPrivate, QMetaType::Void),
        // Slot 'onCancelScanClicked'
        QtMocHelpers::SlotData<void()>(5, 2, QMC::AccessPrivate, QMetaType::Void),
        // Slot 'onSubnetTextChanged'
        QtMocHelpers::SlotData<void(const QString &)>(6, 2, QMC::AccessPrivate, QMetaType::Void, {{
            { QMetaType::QString, 7 },
        }}),
        // Slot 'onWebSocketConnected'
        QtMocHelpers::SlotData<void()>(8, 2, QMC::AccessPrivate, QMetaType::Void),
        // Slot 'onWebSocketDisconnected'
        QtMocHelpers::SlotData<void()>(9, 2, QMC::AccessPrivate, QMetaType::Void),
        // Slot 'onWebSocketError'
        QtMocHelpers::SlotData<void(const QString &)>(10, 2, QMC::AccessPrivate, QMetaType::Void, {{
            { QMetaType::QString, 11 },
        }}),
        // Slot 'onDeviceFound'
        QtMocHelpers::SlotData<void(const DwarfDeviceInfo &)>(12, 2, QMC::AccessPrivate, QMetaType::Void, {{
            { 0x80000000 | 13, 14 },
        }}),
        // Slot 'onScanFinished'
        QtMocHelpers::SlotData<void()>(15, 2, QMC::AccessPrivate, QMetaType::Void),
        // Slot 'onScanProgress'
        QtMocHelpers::SlotData<void(int)>(16, 2, QMC::AccessPrivate, QMetaType::Void, {{
            { QMetaType::Int, 17 },
        }}),
        // Slot 'onDeviceSelected'
        QtMocHelpers::SlotData<void(QListWidgetItem *)>(18, 2, QMC::AccessPrivate, QMetaType::Void, {{
            { 0x80000000 | 19, 20 },
        }}),
        // Slot 'onPipStreamClicked'
        QtMocHelpers::SlotData<void()>(21, 2, QMC::AccessPrivate, QMetaType::Void),
        // Slot 'onCameraSourceTele'
        QtMocHelpers::SlotData<void()>(22, 2, QMC::AccessPrivate, QMetaType::Void),
        // Slot 'onCameraSourceWide'
        QtMocHelpers::SlotData<void()>(23, 2, QMC::AccessPrivate, QMetaType::Void),
        // Slot 'onCameraPhotoClicked'
        QtMocHelpers::SlotData<void()>(24, 2, QMC::AccessPrivate, QMetaType::Void),
        // Slot 'onCameraRecClicked'
        QtMocHelpers::SlotData<void()>(25, 2, QMC::AccessPrivate, QMetaType::Void),
        // Slot 'onExposureModeChanged'
        QtMocHelpers::SlotData<void(int)>(26, 2, QMC::AccessPrivate, QMetaType::Void, {{
            { QMetaType::Int, 27 },
        }}),
        // Slot 'onShutterSliderChanged'
        QtMocHelpers::SlotData<void(int)>(28, 2, QMC::AccessPrivate, QMetaType::Void, {{
            { QMetaType::Int, 29 },
        }}),
        // Slot 'onGainSliderChanged'
        QtMocHelpers::SlotData<void(int)>(30, 2, QMC::AccessPrivate, QMetaType::Void, {{
            { QMetaType::Int, 29 },
        }}),
        // Slot 'onIrCutToggled'
        QtMocHelpers::SlotData<void(bool)>(31, 2, QMC::AccessPrivate, QMetaType::Void, {{
            { QMetaType::Bool, 32 },
        }}),
        // Slot 'onBinningChanged'
        QtMocHelpers::SlotData<void(int)>(33, 2, QMC::AccessPrivate, QMetaType::Void, {{
            { QMetaType::Int, 27 },
        }}),
        // Slot 'onContrastSliderChanged'
        QtMocHelpers::SlotData<void(int)>(34, 2, QMC::AccessPrivate, QMetaType::Void, {{
            { QMetaType::Int, 29 },
        }}),
        // Slot 'onSaturationSliderChanged'
        QtMocHelpers::SlotData<void(int)>(35, 2, QMC::AccessPrivate, QMetaType::Void, {{
            { QMetaType::Int, 29 },
        }}),
        // Slot 'onSharpnessSliderChanged'
        QtMocHelpers::SlotData<void(int)>(36, 2, QMC::AccessPrivate, QMetaType::Void, {{
            { QMetaType::Int, 29 },
        }}),
        // Slot 'onHueSliderChanged'
        QtMocHelpers::SlotData<void(int)>(37, 2, QMC::AccessPrivate, QMetaType::Void, {{
            { QMetaType::Int, 29 },
        }}),
    };
    QtMocHelpers::UintData qt_properties {
    };
    QtMocHelpers::UintData qt_enums {
    };
    return QtMocHelpers::metaObjectData<MainWindow, qt_meta_tag_ZN10MainWindowE_t>(QMC::MetaObjectFlag{}, qt_stringData,
            qt_methods, qt_properties, qt_enums);
}
Q_CONSTINIT const QMetaObject MainWindow::staticMetaObject = { {
    QMetaObject::SuperData::link<QMainWindow::staticMetaObject>(),
    qt_staticMetaObjectStaticContent<qt_meta_tag_ZN10MainWindowE_t>.stringdata,
    qt_staticMetaObjectStaticContent<qt_meta_tag_ZN10MainWindowE_t>.data,
    qt_static_metacall,
    nullptr,
    qt_staticMetaObjectRelocatingContent<qt_meta_tag_ZN10MainWindowE_t>.metaTypes,
    nullptr
} };

void MainWindow::qt_static_metacall(QObject *_o, QMetaObject::Call _c, int _id, void **_a)
{
    auto *_t = static_cast<MainWindow *>(_o);
    if (_c == QMetaObject::InvokeMetaMethod) {
        switch (_id) {
        case 0: _t->onConnectClicked(); break;
        case 1: _t->onCancelConnectClicked(); break;
        case 2: _t->onScanClicked(); break;
        case 3: _t->onCancelScanClicked(); break;
        case 4: _t->onSubnetTextChanged((*reinterpret_cast<std::add_pointer_t<QString>>(_a[1]))); break;
        case 5: _t->onWebSocketConnected(); break;
        case 6: _t->onWebSocketDisconnected(); break;
        case 7: _t->onWebSocketError((*reinterpret_cast<std::add_pointer_t<QString>>(_a[1]))); break;
        case 8: _t->onDeviceFound((*reinterpret_cast<std::add_pointer_t<DwarfDeviceInfo>>(_a[1]))); break;
        case 9: _t->onScanFinished(); break;
        case 10: _t->onScanProgress((*reinterpret_cast<std::add_pointer_t<int>>(_a[1]))); break;
        case 11: _t->onDeviceSelected((*reinterpret_cast<std::add_pointer_t<QListWidgetItem*>>(_a[1]))); break;
        case 12: _t->onPipStreamClicked(); break;
        case 13: _t->onCameraSourceTele(); break;
        case 14: _t->onCameraSourceWide(); break;
        case 15: _t->onCameraPhotoClicked(); break;
        case 16: _t->onCameraRecClicked(); break;
        case 17: _t->onExposureModeChanged((*reinterpret_cast<std::add_pointer_t<int>>(_a[1]))); break;
        case 18: _t->onShutterSliderChanged((*reinterpret_cast<std::add_pointer_t<int>>(_a[1]))); break;
        case 19: _t->onGainSliderChanged((*reinterpret_cast<std::add_pointer_t<int>>(_a[1]))); break;
        case 20: _t->onIrCutToggled((*reinterpret_cast<std::add_pointer_t<bool>>(_a[1]))); break;
        case 21: _t->onBinningChanged((*reinterpret_cast<std::add_pointer_t<int>>(_a[1]))); break;
        case 22: _t->onContrastSliderChanged((*reinterpret_cast<std::add_pointer_t<int>>(_a[1]))); break;
        case 23: _t->onSaturationSliderChanged((*reinterpret_cast<std::add_pointer_t<int>>(_a[1]))); break;
        case 24: _t->onSharpnessSliderChanged((*reinterpret_cast<std::add_pointer_t<int>>(_a[1]))); break;
        case 25: _t->onHueSliderChanged((*reinterpret_cast<std::add_pointer_t<int>>(_a[1]))); break;
        default: ;
        }
    }
}

const QMetaObject *MainWindow::metaObject() const
{
    return QObject::d_ptr->metaObject ? QObject::d_ptr->dynamicMetaObject() : &staticMetaObject;
}

void *MainWindow::qt_metacast(const char *_clname)
{
    if (!_clname) return nullptr;
    if (!strcmp(_clname, qt_staticMetaObjectStaticContent<qt_meta_tag_ZN10MainWindowE_t>.strings))
        return static_cast<void*>(this);
    return QMainWindow::qt_metacast(_clname);
}

int MainWindow::qt_metacall(QMetaObject::Call _c, int _id, void **_a)
{
    _id = QMainWindow::qt_metacall(_c, _id, _a);
    if (_id < 0)
        return _id;
    if (_c == QMetaObject::InvokeMetaMethod) {
        if (_id < 26)
            qt_static_metacall(this, _c, _id, _a);
        _id -= 26;
    }
    if (_c == QMetaObject::RegisterMethodArgumentMetaType) {
        if (_id < 26)
            *reinterpret_cast<QMetaType *>(_a[0]) = QMetaType();
        _id -= 26;
    }
    return _id;
}
QT_WARNING_POP
