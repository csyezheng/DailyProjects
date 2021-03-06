
#include "pch.h"
#include "LuaStack.h"
#include "LuaFunction.h"
#include "LuaVM.h"
#include "GCObject.h"

LuaStackFrame::LuaStackFrame(LuaStack *_stack, Function *_func, int paramBase, int paramCount):
    stack(_stack), func(_func), ip(0), localBase(paramBase + paramCount), tempCount(0), tempExtCount(0){ 
    int localCount = 0, argCount = 0;
    if (func != NULL && func->funcType == Function::FT_Lua) {
        localCount = static_cast<LuaFunction*>(func)->meta->localCount;
        argCount = static_cast<LuaFunction*>(func)->meta->argCount;
    }
    tempBase = localBase + localCount;
    varParamBase = localBase - (paramCount - argCount);
    stack->m_values.resize(tempBase, LuaValue::NIL);
    {
        auto iter = stack->m_values.begin();
        copy(iter + paramBase, iter + paramBase + argCount, iter + localBase);
    }
}

//===== LuaStack =====
void LuaStack::pushFrame(Function *func, int paramBase, int paramCount) {
    m_frames.push_back(new LuaStackFrame(this, func, paramBase, paramCount));
    if (func != NULL && func->funcType == Function::FT_Lua) {
        int level = static_cast<LuaFunction*>(func)->meta->level;
        if ((int)m_framesOfLevel.size() <= level) m_framesOfLevel.resize(level + 1);
        m_framesOfLevel[level].push_back(m_frames.back());
    }
}
void LuaStack::popFrame() {
    auto func = m_frames.back()->func;
    if (func != NULL && func->funcType == Function::FT_Lua) {
        int level = static_cast<LuaFunction*>(func)->meta->level;
        m_framesOfLevel[level].pop_back();
    }

    delete m_frames.back();
    m_frames.pop_back();
}
LuaStackFrame* LuaStack::topFrameOfLevel(int level) {
    return m_framesOfLevel[level].back();
}
LuaStack::LuaStack():
    GCObject(OT_Stack) {
    m_values.reserve(32 * 1024); // FIXME
    pushFrame(NULL, 0, 0);
    LuaVM::instance()->getGCObjManager()->linkObject(this);
}
LuaStack::~LuaStack() {
    popFrame();
    ASSERT(m_frames.empty());
}

void LuaStack::collectGCObject(vector<GCObject*>& unscaned) {
    for (auto &v : m_values) {
        if (auto p = v.gcAccess()) unscaned.push_back(p);
    }
    for (auto frame : m_frames) {
        if (frame->func == NULL) continue;
        if (auto p = frame->func->gcAccess()) unscaned.push_back(p);
    }
}
