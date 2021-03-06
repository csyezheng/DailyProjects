package lexical

import scala.collection.immutable

trait IToken extends Ordered[IToken] {
  def id : Int
  def name : String
  def value : Any
  def locationText : String
  override def equals(other : Any) = other match {
    case o : IToken => id == o.id
    case _ => false
  }
  override def hashCode() = id.hashCode()
  def compare(that : IToken) : Int = id.compare(that.id)
}

object IToken {
  val EOF = new FastToken(0, "EOF", null)
  val ERROR = new FastToken(1, "ERROR", null)
  val EMPTY = new FastToken(2, "ε", null)

  val NextTokenID = 3
}

final class FastToken(val id : Int, val name : String, val value : Any) extends IToken {
  override def toString = s"Token($name,$value)"
  def locationText : String = "<Unkown>"
}

abstract class FileToken(val id : Int, val name : String, val value : Any, val startLoc : (Int, Int), val endLoc : (Int, Int)) extends IToken {
  override def toString = s"Token($name,$value,start=$startLoc,end=$endLoc)"
}

trait ITokenFactory {
  def create(id : Int, name : String, value : Any, lexeme : String) : IToken
  def eof() : IToken
  def error(lexeme : String) : IToken
}

final class FastTokenFactory extends ITokenFactory {
  def create(id : Int, name : String, value : Any, lexeme : String) : IToken = new FastToken(id, name, value)
  def eof() : IToken = IToken.EOF
  def error(lexeme : String) : IToken = new FastToken(IToken.ERROR.id, IToken.ERROR.name, lexeme)
}

final class FileTokenFactory extends ITokenFactory {
  var line = 1
  var column = 1
  val lastLineText = new StringBuilder()

  private def nextLocation(lexeme : String) : ((Int, Int), (Int, Int)) = {
    val startLoc = (line, column)
    lexeme.foreach {
      case '\n' =>
        line += 1
        column = 1
        lastLineText.clear()
      case c =>
        column += 1
        lastLineText += c
    }
    (startLoc, (line, column))
  }

  private def getLocationText(start : (Int, Int), end : (Int, Int)) : String = {
    if (line < start._1 || line > end._1) return "<Unkown>"

    def getMark(column : Int) = if (column >= start._2 && column < end._2) '~' else ' '

    val lineText = lastLineText.toString()
    s"$lineText\n${new String((1 to column).map(getMark).toArray)}"
  }

  def create(id : Int, name : String, value : Any, lexeme : String) : IToken = {
    val (startLoc, endLoc) = nextLocation(lexeme)
    new FileToken(id, name, value, startLoc, endLoc) {
      def locationText : String = getLocationText(this.startLoc, this.endLoc)
    }
  }

  def eof() : IToken = IToken.EOF

  def error(lexeme : String) : IToken = {
    val (startLoc, endLoc) = nextLocation(lexeme)
    new FileToken(IToken.ERROR.id, IToken.ERROR.name, lexeme, startLoc, endLoc) {
      def locationText : String = getLocationText(this.startLoc, this.endLoc)
    }
  }
}

trait IScanner extends Iterator[IToken]

final class TokenFAStateAttribute(
  val priority : Int,
  val id : Int,
  val name : String,
  val lexemeHandler : (String) => Any) extends IFAStateAttribute {
  override def toString = name
}

object IgnoreHandler extends (String => Any) {
  val IgnoreResult = {}
  def apply(s : String) : Any = IgnoreResult
}

abstract class ScannerBuilder {
  def _create(source : ICharSource, tokenFactory : ITokenFactory) : IScanner

  private final var nextPriority = 0
  private final var nextTokenID = IToken.NextTokenID
  private final var name2Token = immutable.Map[String, IToken]()
  private final var regexNFAs : List[TokenizedNFA] = Nil

  def create(source : ICharSource, tokenFactory : ITokenFactory = new FileTokenFactory) : Iterator[IToken] = {
    _create(source, tokenFactory).filter(_.value != IgnoreHandler.IgnoreResult)
  }

  def token(name : String, pattern : String, lexemeHandler : (String) => Any) : this.type = {
    regexNFAs = TokenizedNFA.fromPattern(pattern, new TokenFAStateAttribute(nextPriority, nextTokenID, name, lexemeHandler)) :: regexNFAs
    name2Token += ((name, new FastToken(nextTokenID, name, null)))
    nextPriority -= 1
    nextTokenID += 1
    this
  }

  def token(name : String) : this.type = token(name, RegexAST.escape(name), identity)

  def literals(names : String*) : this.type = {
    names.foreach(token)
    this
  }

  def getToken(name : String) = name2Token(name)

  protected lazy val dfaEmulator : TokenizedDFAEmulator = {
    val resultNFA = regexNFAs.tail.fold(regexNFAs.head) { (r, nfa) => r | nfa}
    resultNFA.toDFAEmulator.optimized
  }

  object Implicits {
    implicit def string2Token(name : String) : IToken = getToken(name)
  }
}