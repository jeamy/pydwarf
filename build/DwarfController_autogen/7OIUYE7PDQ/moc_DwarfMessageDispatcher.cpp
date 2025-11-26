/****************************************************************************
** Meta object code from reading C++ file 'DwarfMessageDispatcher.h'
**
** Created by: The Qt Meta Object Compiler version 69 (Qt 6.10.1)
**
** WARNING! All changes made in this file will be lost!
*****************************************************************************/

#include "../../../src/net/DwarfMessageDispatcher.h"
#include <QtCore/qmetatype.h>

#include <QtCore/qtmochelpers.h>

#include <memory>


#include <QtCore/qxptype_traits.h>
#if !defined(Q_MOC_OUTPUT_REVISION)
#error "The header file 'DwarfMessageDispatcher.h' doesn't include <QObject>."
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
struct qt_meta_tag_ZN22DwarfMessageDispatcherE_t {};
} // unnamed namespace

template <> constexpr inline auto DwarfMessageDispatcher::qt_create_metaobjectdata<qt_meta_tag_ZN22DwarfMessageDispatcherE_t>()
{
    namespace QMC = QtMocConstants;
    QtMocHelpers::StringRefStorage qt_stringData {
        "DwarfMessageDispatcher",
        "astroMessage",
        "",
        "std::uint32_t",
        "cmd",
        "data",
        "systemMessage",
        "rgbPowerMessage",
        "motorMessage",
        "trackMessage",
        "focusMessage",
        "notifyMessage",
        "panoramaMessage",
        "unknownMessage",
        "moduleId",
        "dispatch"
    };

    QtMocHelpers::UintData qt_methods {
        // Signal 'astroMessage'
        QtMocHelpers::SignalData<void(std::uint32_t, const QByteArray &)>(1, 2, QMC::AccessPublic, QMetaType::Void, {{
            { 0x80000000 | 3, 4 }, { QMetaType::QByteArray, 5 },
        }}),
        // Signal 'systemMessage'
        QtMocHelpers::SignalData<void(std::uint32_t, const QByteArray &)>(6, 2, QMC::AccessPublic, QMetaType::Void, {{
            { 0x80000000 | 3, 4 }, { QMetaType::QByteArray, 5 },
        }}),
        // Signal 'rgbPowerMessage'
        QtMocHelpers::SignalData<void(std::uint32_t, const QByteArray &)>(7, 2, QMC::AccessPublic, QMetaType::Void, {{
            { 0x80000000 | 3, 4 }, { QMetaType::QByteArray, 5 },
        }}),
        // Signal 'motorMessage'
        QtMocHelpers::SignalData<void(std::uint32_t, const QByteArray &)>(8, 2, QMC::AccessPublic, QMetaType::Void, {{
            { 0x80000000 | 3, 4 }, { QMetaType::QByteArray, 5 },
        }}),
        // Signal 'trackMessage'
        QtMocHelpers::SignalData<void(std::uint32_t, const QByteArray &)>(9, 2, QMC::AccessPublic, QMetaType::Void, {{
            { 0x80000000 | 3, 4 }, { QMetaType::QByteArray, 5 },
        }}),
        // Signal 'focusMessage'
        QtMocHelpers::SignalData<void(std::uint32_t, const QByteArray &)>(10, 2, QMC::AccessPublic, QMetaType::Void, {{
            { 0x80000000 | 3, 4 }, { QMetaType::QByteArray, 5 },
        }}),
        // Signal 'notifyMessage'
        QtMocHelpers::SignalData<void(std::uint32_t, const QByteArray &)>(11, 2, QMC::AccessPublic, QMetaType::Void, {{
            { 0x80000000 | 3, 4 }, { QMetaType::QByteArray, 5 },
        }}),
        // Signal 'panoramaMessage'
        QtMocHelpers::SignalData<void(std::uint32_t, const QByteArray &)>(12, 2, QMC::AccessPublic, QMetaType::Void, {{
            { 0x80000000 | 3, 4 }, { QMetaType::QByteArray, 5 },
        }}),
        // Signal 'unknownMessage'
        QtMocHelpers::SignalData<void(std::uint32_t, std::uint32_t, const QByteArray &)>(13, 2, QMC::AccessPublic, QMetaType::Void, {{
            { 0x80000000 | 3, 14 }, { 0x80000000 | 3, 4 }, { QMetaType::QByteArray, 5 },
        }}),
        // Slot 'dispatch'
        QtMocHelpers::SlotData<void(std::uint32_t, std::uint32_t, const QByteArray &)>(15, 2, QMC::AccessPublic, QMetaType::Void, {{
            { 0x80000000 | 3, 14 }, { 0x80000000 | 3, 4 }, { QMetaType::QByteArray, 5 },
        }}),
    };
    QtMocHelpers::UintData qt_properties {
    };
    QtMocHelpers::UintData qt_enums {
    };
    return QtMocHelpers::metaObjectData<DwarfMessageDispatcher, qt_meta_tag_ZN22DwarfMessageDispatcherE_t>(QMC::MetaObjectFlag{}, qt_stringData,
            qt_methods, qt_properties, qt_enums);
}
Q_CONSTINIT const QMetaObject DwarfMessageDispatcher::staticMetaObject = { {
    QMetaObject::SuperData::link<QObject::staticMetaObject>(),
    qt_staticMetaObjectStaticContent<qt_meta_tag_ZN22DwarfMessageDispatcherE_t>.stringdata,
    qt_staticMetaObjectStaticContent<qt_meta_tag_ZN22DwarfMessageDispatcherE_t>.data,
    qt_static_metacall,
    nullptr,
    qt_staticMetaObjectRelocatingContent<qt_meta_tag_ZN22DwarfMessageDispatcherE_t>.metaTypes,
    nullptr
} };

void DwarfMessageDispatcher::qt_static_metacall(QObject *_o, QMetaObject::Call _c, int _id, void **_a)
{
    auto *_t = static_cast<DwarfMessageDispatcher *>(_o);
    if (_c == QMetaObject::InvokeMetaMethod) {
        switch (_id) {
        case 0: _t->astroMessage((*reinterpret_cast<std::add_pointer_t<std::uint32_t>>(_a[1])),(*reinterpret_cast<std::add_pointer_t<QByteArray>>(_a[2]))); break;
        case 1: _t->systemMessage((*reinterpret_cast<std::add_pointer_t<std::uint32_t>>(_a[1])),(*reinterpret_cast<std::add_pointer_t<QByteArray>>(_a[2]))); break;
        case 2: _t->rgbPowerMessage((*reinterpret_cast<std::add_pointer_t<std::uint32_t>>(_a[1])),(*reinterpret_cast<std::add_pointer_t<QByteArray>>(_a[2]))); break;
        case 3: _t->motorMessage((*reinterpret_cast<std::add_pointer_t<std::uint32_t>>(_a[1])),(*reinterpret_cast<std::add_pointer_t<QByteArray>>(_a[2]))); break;
        case 4: _t->trackMessage((*reinterpret_cast<std::add_pointer_t<std::uint32_t>>(_a[1])),(*reinterpret_cast<std::add_pointer_t<QByteArray>>(_a[2]))); break;
        case 5: _t->focusMessage((*reinterpret_cast<std::add_pointer_t<std::uint32_t>>(_a[1])),(*reinterpret_cast<std::add_pointer_t<QByteArray>>(_a[2]))); break;
        case 6: _t->notifyMessage((*reinterpret_cast<std::add_pointer_t<std::uint32_t>>(_a[1])),(*reinterpret_cast<std::add_pointer_t<QByteArray>>(_a[2]))); break;
        case 7: _t->panoramaMessage((*reinterpret_cast<std::add_pointer_t<std::uint32_t>>(_a[1])),(*reinterpret_cast<std::add_pointer_t<QByteArray>>(_a[2]))); break;
        case 8: _t->unknownMessage((*reinterpret_cast<std::add_pointer_t<std::uint32_t>>(_a[1])),(*reinterpret_cast<std::add_pointer_t<std::uint32_t>>(_a[2])),(*reinterpret_cast<std::add_pointer_t<QByteArray>>(_a[3]))); break;
        case 9: _t->dispatch((*reinterpret_cast<std::add_pointer_t<std::uint32_t>>(_a[1])),(*reinterpret_cast<std::add_pointer_t<std::uint32_t>>(_a[2])),(*reinterpret_cast<std::add_pointer_t<QByteArray>>(_a[3]))); break;
        default: ;
        }
    }
    if (_c == QMetaObject::IndexOfMethod) {
        if (QtMocHelpers::indexOfMethod<void (DwarfMessageDispatcher::*)(std::uint32_t , const QByteArray & )>(_a, &DwarfMessageDispatcher::astroMessage, 0))
            return;
        if (QtMocHelpers::indexOfMethod<void (DwarfMessageDispatcher::*)(std::uint32_t , const QByteArray & )>(_a, &DwarfMessageDispatcher::systemMessage, 1))
            return;
        if (QtMocHelpers::indexOfMethod<void (DwarfMessageDispatcher::*)(std::uint32_t , const QByteArray & )>(_a, &DwarfMessageDispatcher::rgbPowerMessage, 2))
            return;
        if (QtMocHelpers::indexOfMethod<void (DwarfMessageDispatcher::*)(std::uint32_t , const QByteArray & )>(_a, &DwarfMessageDispatcher::motorMessage, 3))
            return;
        if (QtMocHelpers::indexOfMethod<void (DwarfMessageDispatcher::*)(std::uint32_t , const QByteArray & )>(_a, &DwarfMessageDispatcher::trackMessage, 4))
            return;
        if (QtMocHelpers::indexOfMethod<void (DwarfMessageDispatcher::*)(std::uint32_t , const QByteArray & )>(_a, &DwarfMessageDispatcher::focusMessage, 5))
            return;
        if (QtMocHelpers::indexOfMethod<void (DwarfMessageDispatcher::*)(std::uint32_t , const QByteArray & )>(_a, &DwarfMessageDispatcher::notifyMessage, 6))
            return;
        if (QtMocHelpers::indexOfMethod<void (DwarfMessageDispatcher::*)(std::uint32_t , const QByteArray & )>(_a, &DwarfMessageDispatcher::panoramaMessage, 7))
            return;
        if (QtMocHelpers::indexOfMethod<void (DwarfMessageDispatcher::*)(std::uint32_t , std::uint32_t , const QByteArray & )>(_a, &DwarfMessageDispatcher::unknownMessage, 8))
            return;
    }
}

const QMetaObject *DwarfMessageDispatcher::metaObject() const
{
    return QObject::d_ptr->metaObject ? QObject::d_ptr->dynamicMetaObject() : &staticMetaObject;
}

void *DwarfMessageDispatcher::qt_metacast(const char *_clname)
{
    if (!_clname) return nullptr;
    if (!strcmp(_clname, qt_staticMetaObjectStaticContent<qt_meta_tag_ZN22DwarfMessageDispatcherE_t>.strings))
        return static_cast<void*>(this);
    return QObject::qt_metacast(_clname);
}

int DwarfMessageDispatcher::qt_metacall(QMetaObject::Call _c, int _id, void **_a)
{
    _id = QObject::qt_metacall(_c, _id, _a);
    if (_id < 0)
        return _id;
    if (_c == QMetaObject::InvokeMetaMethod) {
        if (_id < 10)
            qt_static_metacall(this, _c, _id, _a);
        _id -= 10;
    }
    if (_c == QMetaObject::RegisterMethodArgumentMetaType) {
        if (_id < 10)
            *reinterpret_cast<QMetaType *>(_a[0]) = QMetaType();
        _id -= 10;
    }
    return _id;
}

// SIGNAL 0
void DwarfMessageDispatcher::astroMessage(std::uint32_t _t1, const QByteArray & _t2)
{
    QMetaObject::activate<void>(this, &staticMetaObject, 0, nullptr, _t1, _t2);
}

// SIGNAL 1
void DwarfMessageDispatcher::systemMessage(std::uint32_t _t1, const QByteArray & _t2)
{
    QMetaObject::activate<void>(this, &staticMetaObject, 1, nullptr, _t1, _t2);
}

// SIGNAL 2
void DwarfMessageDispatcher::rgbPowerMessage(std::uint32_t _t1, const QByteArray & _t2)
{
    QMetaObject::activate<void>(this, &staticMetaObject, 2, nullptr, _t1, _t2);
}

// SIGNAL 3
void DwarfMessageDispatcher::motorMessage(std::uint32_t _t1, const QByteArray & _t2)
{
    QMetaObject::activate<void>(this, &staticMetaObject, 3, nullptr, _t1, _t2);
}

// SIGNAL 4
void DwarfMessageDispatcher::trackMessage(std::uint32_t _t1, const QByteArray & _t2)
{
    QMetaObject::activate<void>(this, &staticMetaObject, 4, nullptr, _t1, _t2);
}

// SIGNAL 5
void DwarfMessageDispatcher::focusMessage(std::uint32_t _t1, const QByteArray & _t2)
{
    QMetaObject::activate<void>(this, &staticMetaObject, 5, nullptr, _t1, _t2);
}

// SIGNAL 6
void DwarfMessageDispatcher::notifyMessage(std::uint32_t _t1, const QByteArray & _t2)
{
    QMetaObject::activate<void>(this, &staticMetaObject, 6, nullptr, _t1, _t2);
}

// SIGNAL 7
void DwarfMessageDispatcher::panoramaMessage(std::uint32_t _t1, const QByteArray & _t2)
{
    QMetaObject::activate<void>(this, &staticMetaObject, 7, nullptr, _t1, _t2);
}

// SIGNAL 8
void DwarfMessageDispatcher::unknownMessage(std::uint32_t _t1, std::uint32_t _t2, const QByteArray & _t3)
{
    QMetaObject::activate<void>(this, &staticMetaObject, 8, nullptr, _t1, _t2, _t3);
}
QT_WARNING_POP
