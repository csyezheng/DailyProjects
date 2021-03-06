package parsing

import scala.collection.mutable

abstract class LRParser[ActionT] extends IParser {
  def actionTable : ILRActionTable[ActionT]
  def gotoTable : ILRGotoTable
}

object LRAction {
  sealed abstract class Action
  case class Shift(targetState : Int) extends Action
  case class Reduce(production : IProduction) extends Action
  case class Accept(production : IProduction) extends Action
}

trait ILRActionTable[ActionT] extends ((Int, Int) => ActionT) {
}
final class LRActionTable[ActionT](table : Array[Array[ActionT]]) extends ILRActionTable[ActionT] {
  def apply(state : Int, tid : Int) = table(state)(tid)
}
final class CompressedLRActionTable[ActionT](_table : Array[Array[ActionT]]) extends ILRActionTable[ActionT] {
  val (table, state2Row) = {
    val state2Row = Array.fill(_table.length)(0)
    var id = 0
    ((for ((row, states) <- _table.zipWithIndex.groupBy(_._1.toList).iterator)
    yield {
      for ((_, state) <- states) state2Row(state) = id
      id += 1
      row
    }).toArray, state2Row)
  }

  def apply(state : Int, tid : Int) = table(state2Row(state))(tid)
}

trait ILRGotoTable extends ((Int, String) => Int) {
  def tryApply(state : Int, nonTerm : String) : Option[Int]
}
final class LRGotoTable(table : Array[mutable.HashMap[String, Int]]) extends ILRGotoTable {
  def apply(state : Int, nonTerm : String) = table(state)(nonTerm)
  def tryApply(state : Int, nonTerm : String) = table(state).get(nonTerm)
}
final class CompressedLRGotoTable(_table : Array[mutable.HashMap[String, Int]]) extends ILRGotoTable {
  val (table, state2Row) = {
    val state2Row = Array.fill(_table.length)(0)
    var id = 0
    ((for ((row, states) <- _table.zipWithIndex.groupBy(_._1).iterator)
    yield {
      for ((_, state) <- states) state2Row(state) = id
      id += 1
      row
    }).toArray, state2Row)
  }

  def apply(state : Int, nonTerm : String) = table(state2Row(state))(nonTerm)
  def tryApply(state : Int, nonTerm : String) : Option[Int] = table(state2Row(state)).get(nonTerm)
}
