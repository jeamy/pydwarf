/****************************************************************************
** Meta object code from reading C++ file 'DwarfWebSocketClient.h'
**
** Created by: The Qt Meta Object Compiler version 69 (Qt 6.10.1)
**
** WARNING! All changes made in this file will be lost!
*****************************************************************************/

#include "../../../src/net/DwarfWebSocketClient.h"
#include <QtCore/qmetatype.h>

#include <QtCore/qtmochelpers.h>

#include <memory>


#include <QtCore/qxptype_traits.h>
#if !defined(Q_MOC_OUTPUT_REVISION)
#error "The header file 'DwarfWebSocketClient.h' doesn't include <QObject>."
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
struct qt_meta_tag_ZN20DwarfWebSocketClientE_t {};
} // unnamed namespace

template <> constexpr inline auto DwarfWebSocketClient::qt_create_metaobjectdata<qt_meta_tag_ZN20DwarfWebSocketClientE_t>()
{
    namespace QMC = QtMocConstants;
    QtMocHelpers::StringRefStorage qt_stringData {
        "DwarfWebSocketClient",
        "connected",
        "",
        "disconnected",
        "messageReceived",
        "uint32_t",
        "moduleId",
        "cmd",
        "data",
        "errorOccurred",
        "error",
        "onConnected",
        "onDisconnected",
        "onBinaryMessageReceived",
        "message",
        "onError",
        "QAbstractSocket::SocketError",
        "sendPing"
    };

    QtMocHelpers::UintData qt_methods {
        // Signal 'connected'
        QtMocHelpers::SignalData<void()>(1, 2, QMC::AccessPublic, QMetaType::Void),
        // Signal 'disconnected'
        QtMocHelpers::SignalData<void()>(3, 2, QMC::AccessPublic, QMetaType::Void),
        // Signal 'messageReceived'
        QtMocHelpers::SignalData<void(uint32_t, uint32_t, const QByteArray &)>(4, 2, QMC::AccessPublic, QMetaType::Void, {{
            { 0x80000000 | 5, 6 }, { 0x80000000 | 5, 7 }, { QMetaType::QByteArray, 8 },
        }}),
        // Signal 'errorOccurred'
        QtMocHelpers::SignalData<void(const QString &)>(9, 2, QMC::AccessPublic, QMetaType::Void, {{
            { QMetaType::QString, 10 },
        }}),
        // Slot 'onConnected'
        QtMocHelpers::SlotData<void()>(11, 2, QMC::AccessPrivate, QMetaType::Void),
        // Slot 'onDisconnected'
        QtMocHelpers::SlotData<void()>(12, 2, QMC::AccessPrivate, QMetaType::Void),
        // Slot 'onBinaryMessageReceived'
        QtMocHelpers::SlotData<void(const QByteArray &)>(13, 2, QMC::AccessPrivate, QMetaType::Void, {{
            { QMetaType::QByteArray, 14 },
        }}),
        // Slot 'onError'
        QtMocHelpers::SlotData<void(QAbstractSocket::SocketError)>(15, 2, QMC::AccessPrivate, QMetaType::Void, {{
            { 0x80000000 | 16, 10 },
        }}),
        // Slot 'sendPing'
        QtMocHelpers::SlotData<void()>(17, 2, QMC::AccessPrivate, QMetaType::Void),
    };
    QtMocHelpers::UintData qt_properties {
    };
    QtMocHelpers::UintData qt_enums {
    };
    return QtMocHelpers::metaObjectData<DwarfWebSocketClient, qt_meta_tag_ZN20DwarfWebSocketClientE_t>(QMC::MetaObjectFlag{}, qt_stringData,
            qt_methods, qt_properties, qt_enums);
}
Q_CONSTINIT const QMetaObject DwarfWebSocketClient::staticMetaObject = { {
    QMetaObject::SuperData::link<QObject::staticMetaObject>(),
    qt_staticMetaObjectStaticContent<qt_meta_tag_ZN20DwarfWebSocketClientE_t>.stringdata,
    qt_staticMetaObjectStaticContent<qt_meta_tag_ZN20DwarfWebSocketClientE_t>.data,
    qt_static_metacall,
    nullptr,
    qt_staticMetaObjectRelocatingContent<qt_meta_tag_ZN20DwarfWebSocketClientE_t>.metaTypes,
    nullptr
} };

void DwarfWebSocketClient::qt_static_metacall(QObject *_o, QMetaObject::Call _c, int _id, void **_a)
{
    auto *_t = static_cast<DwarfWebSocketClient *>(_o);
    if (_c == QMetaObject::InvokeMetaMethod) {
        switch (_id) {
        case 0: _t->connected(); break;
        case 1: _t->disconnected(); break;
        case 2: _t->messageReceived((*reinterpret_cast<std::add_pointer_t<uint32_t>>(_a[1])),(*reinterpret_cast<std::add_pointer_t<uint32_t>>(_a[2])),(*reinterpret_cast<std::add_pointer_t<QByteArray>>(_a[3]))); break;
        case 3: _t->errorOccurred((*reinterpret_cast<std::add_pointer_t<QString>>(_a[1]))); break;
        case 4: _t->onConnected(); break;
        case 5: _t->onDisconnected(); break;
        case 6: _t->onBinaryMessageReceived((*reinterpret_cast<std::add_pointer_t<QByteArray>>(_a[1]))); break;
        case 7: _t->onError((*reinterpret_cast<std::add_pointer_t<QAbstractSocket::SocketError>>(_a[1]))); break;
        case 8: _t->sendPing(); break;
        default: ;
        }
    }
    if (_c == QMetaObject::RegisterMethodArgumentMetaType) {
        switch (_id) {
        default: *reinterpret_cast<QMetaType *>(_a[0]) = QMetaType(); break;
        case 7:
            switch (*reinterpret_cast<int*>(_a[1])) {
            default: *reinterpret_cast<QMetaType *>(_a[0]) = QMetaType(); break;
            case 0:
                *reinterpret_cast<QMetaType *>(_a[0]) = QMetaType::fromType< QAbstractSocket::SocketError >(); break;
            }
            break;
        }
    }
    if (_c == QMetaObject::IndexOfMethod) {
        if (QtMocHelpers::indexOfMethod<void (DwarfWebSocketClient::*)()>(_a, &DwarfWebSocketClient::connected, 0))
            return;
        if (QtMocHelpers::indexOfMethod<void (DwarfWebSocketClient::*)()>(_a, &DwarfWebSocketClient::disconnected, 1))
            return;
        if (QtMocHelpers::indexOfMethod<void (DwarfWebSocketClient::*)(uint32_t , uint32_t , const QByteArray & )>(_a, &DwarfWebSocketClient::messageReceived, 2))
            return;
        if (QtMocHelpers::indexOfMethod<void (DwarfWebSocketClient::*)(const QString & )>(_a, &DwarfWebSocketClient::errorOccurred, 3))
            return;
    }
}

const QMetaObject *DwarfWebSocketClient::metaObject() const
{
    return QObject::d_ptr->metaObject ? QObject::d_ptr->dynamicMetaObject() : &staticMetaObject;
}

void *DwarfWebSocketClient::qt_metacast(const char *_clname)
{
    if (!_clname) return nullptr;
    if (!strcmp(_clname, qt_staticMetaObjectStaticContent<qt_meta_tag_ZN20DwarfWebSocketClientE_t>.strings))
        return static_cast<void*>(this);
    return QObject::qt_metacast(_clname);
}

int DwarfWebSocketClient::qt_metacall(QMetaObject::Call _c, int _id, void **_a)
{
    _id = QObject::qt_metacall(_c, _id, _a);
    if (_id < 0)
        return _id;
    if (_c == QMetaObject::InvokeMetaMethod) {
        if (_id < 9)
            qt_static_metacall(this, _c, _id, _a);
        _id -= 9;
    }
    if (_c == QMetaObject::RegisterMethodArgumentMetaType) {
        if (_id < 9)
            qt_static_metacall(this, _c, _id, _a);
        _id -= 9;
    }
    return _id;
}

// SIGNAL 0
void DwarfWebSocketClient::connected()
{
    QMetaObject::activate(this, &staticMetaObject, 0, nullptr);
}

// SIGNAL 1
void DwarfWebSocketClient::disconnected()
{
    QMetaObject::activate(this, &staticMetaObject, 1, nullptr);
}

// SIGNAL 2
void DwarfWebSocketClient::messageReceived(uint32_t _t1, uint32_t _t2, const QByteArray & _t3)
{
    QMetaObject::activate<void>(this, &staticMetaObject, 2, nullptr, _t1, _t2, _t3);
}

// SIGNAL 3
void DwarfWebSocketClient::errorOccurred(const QString & _t1)
{
    QMetaObject::activate<void>(this, &staticMetaObject, 3, nullptr, _t1);
}
QT_WARNING_POP
