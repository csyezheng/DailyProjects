#include "pch.h"
#include "SDisassembler.h"
#include "ByteCodeDefinition.h"

uint8_t* SDisassembler::disassembleIns(ostream &so, uint8_t *ins) {
    switch (ins[0]) {
        case BCE_LoadBool:
            so << format("loadbool %d", reinterpret_cast<ByteCode<BCE_LoadBool>*>(ins)->value);
            return ins + sizeof(ByteCode<BCE_LoadBool>);
        case BCE_LoadInt:
            so << format("loadint %d", reinterpret_cast<ByteCode<BCE_LoadInt>*>(ins)->value);
            return ins + sizeof(ByteCode<BCE_LoadInt>);
        case BCE_LoadDouble:
            so << format("loaddouble %f", reinterpret_cast<ByteCode<BCE_LoadDouble>*>(ins)->value);
            return ins + sizeof(ByteCode<BCE_LoadDouble>);
        case BCE_LoadConstant:
            so << format("loadk %d", reinterpret_cast<ByteCode<BCE_LoadConstant>*>(ins)->kindex);
            return ins + sizeof(ByteCode<BCE_LoadConstant>);
        case BCE_LoadGlobal:
            so << format("loadg %d", reinterpret_cast<ByteCode<BCE_LoadGlobal>*>(ins)->gindex);
            return ins + sizeof(ByteCode<BCE_LoadGlobal>);
        case BCE_StoreGlobal:
            so << format("storeg %d", reinterpret_cast<ByteCode<BCE_StoreGlobal>*>(ins)->gindex);
            return ins + sizeof(ByteCode<BCE_StoreGlobal>);
        case BCE_LoadLocal:
            so << format("loadl %d", reinterpret_cast<ByteCode<BCE_LoadLocal>*>(ins)->lindex);
            return ins + sizeof(ByteCode<BCE_LoadLocal>);
        case BCE_StoreLocal:
            so << format("storel %d", reinterpret_cast<ByteCode<BCE_StoreLocal>*>(ins)->lindex);
            return ins + sizeof(ByteCode<BCE_StoreLocal>);
        case BCE_LoadFree:
            so << format("loadf %d,%d", 
                    reinterpret_cast<ByteCode<BCE_LoadFree>*>(ins)->envIndex,
                    reinterpret_cast<ByteCode<BCE_LoadFree>*>(ins)->index);
            return ins + sizeof(ByteCode<BCE_LoadFree>);
        case BCE_LoadFree1:
            so << format("loadf1 %d", reinterpret_cast<ByteCode<BCE_LoadFree1>*>(ins)->index);
            return ins + sizeof(ByteCode<BCE_LoadFree1>);
        case BCE_LoadFree2:
            so << format("loadf2 %d", reinterpret_cast<ByteCode<BCE_LoadFree2>*>(ins)->index);
            return ins + sizeof(ByteCode<BCE_LoadFree2>);
        case BCE_LoadFree3:
            so << format("loadf3 %d", reinterpret_cast<ByteCode<BCE_LoadFree3>*>(ins)->index);
            return ins + sizeof(ByteCode<BCE_LoadFree3>);
        case BCE_StoreFree:
            so << format("storef %d,%d", 
                    reinterpret_cast<ByteCode<BCE_StoreFree>*>(ins)->envIndex,
                    reinterpret_cast<ByteCode<BCE_StoreFree>*>(ins)->index);
            return ins + sizeof(ByteCode<BCE_StoreFree>);
        case BCE_StoreFree1:
            so << format("storef1 %d", reinterpret_cast<ByteCode<BCE_StoreFree1>*>(ins)->index);
            return ins + sizeof(ByteCode<BCE_StoreFree1>);
        case BCE_StoreFree2:
            so << format("storef2 %d", reinterpret_cast<ByteCode<BCE_StoreFree2>*>(ins)->index);
            return ins + sizeof(ByteCode<BCE_StoreFree2>);
        case BCE_StoreFree3:
            so << format("storef3 %d", reinterpret_cast<ByteCode<BCE_StoreFree3>*>(ins)->index);
            return ins + sizeof(ByteCode<BCE_StoreFree3>);
        case BCE_LoadFunc:
            so << format("loadfunc %d", reinterpret_cast<ByteCode<BCE_LoadFunc>*>(ins)->findex);
            return ins + sizeof(ByteCode<BCE_LoadFunc>);
        case BCE_Pop:
            so << format("pop");
            return ins + sizeof(ByteCode<BCE_Pop>);
        case BCE_Jmp:
            so << format("jmp %d", reinterpret_cast<ByteCode<BCE_Jmp>*>(ins)->target);
            return ins + sizeof(ByteCode<BCE_Jmp>);
        case BCE_TrueJmp:
            so << format("tjmp %d", reinterpret_cast<ByteCode<BCE_TrueJmp>*>(ins)->target);
            return ins + sizeof(ByteCode<BCE_TrueJmp>);
        case BCE_Tail:
            so << format("tail");
            return ins + sizeof(ByteCode<BCE_Tail>);
        case BCE_Call:
            so << format("call %d", reinterpret_cast<ByteCode<BCE_Call>*>(ins)->actualCount);
            return ins + sizeof(ByteCode<BCE_Call>);
        case BCE_LoadClass:
            so << format("loadclass %d", reinterpret_cast<ByteCode<BCE_LoadClass>*>(ins)->cindex);
            return ins + sizeof(ByteCode<BCE_LoadClass>);
        case BCE_LoadMethod:
            so << format("loadmethod %d,%d", 
                    reinterpret_cast<ByteCode<BCE_LoadMethod>*>(ins)->envIndex,
                    reinterpret_cast<ByteCode<BCE_LoadMethod>*>(ins)->index);
            return ins + sizeof(ByteCode<BCE_LoadMethod>);
        case BCE_LoadCachedMethod:
            so << format("loadcachedmethod");
            return ins + sizeof(ByteCode<BCE_LoadCachedMethod>);
        case BCE_GetField:
            so << format("getfield %d", reinterpret_cast<ByteCode<BCE_GetField>*>(ins)->kindex);
            return ins + sizeof(ByteCode<BCE_GetField>);
        case BCE_GetCachedField:
            so << "getcachedfield";
            return ins + sizeof(ByteCode<BCE_GetCachedField>);
        case BCE_GetMethod:
            so << format("getmethod %d", reinterpret_cast<ByteCode<BCE_GetMethod>*>(ins)->kindex);
            return ins + sizeof(ByteCode<BCE_GetMethod>);
        case BCE_GetCachedMethod:
            so << "getcachedmethod";
            return ins + sizeof(ByteCode<BCE_GetCachedMethod>);
        default:
            ASSERT(0);
            return ins;
    }
}

static void writeTab(ostream &so, int indent) {
    for (int i = 0; i < indent; ++i) so << '\t';
}

void SDisassembler::disassemble(ostream &so, int indent, uint8_t *codes, int codeSize) {
    for (uint8_t *pc = codes, *cend = codes + codeSize; pc < cend; ) {
        writeTab(so, indent);
        so << format("%-3d: ", int(pc - codes));
        pc = disassembleIns(so, pc);
        so << '\n';
    }
}