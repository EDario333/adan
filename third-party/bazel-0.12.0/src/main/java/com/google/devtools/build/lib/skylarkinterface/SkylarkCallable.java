// Copyright 2014 The Bazel Authors. All rights reserved.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//    http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
package com.google.devtools.build.lib.skylarkinterface;

import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

/**
 * A marker interface for Java methods which can be called from Skylark.
 *
 * <p>Methods annotated with this annotation are expected to meet certain requirements which
 * are enforced by an annotation processor:</p>
 * <ul>
 * <li>The method must be public.</li>
 * <li>If structField=true, there must be zero user-supplied parameters.</li>
 * <li>Method parameters must be supplied in the following order:
 *   <pre>method([positionals]*[other user-args](Location)(FuncallExpression)(Envrionment))</pre>
 *   where Location, FuncallExpression, and Environment are supplied by the interpreter if and
 *   only if useLocation, useAst, and useEnvironment are specified, respectively.
*  </li>
 * <li>
 *   The number of method parameters much match the number of annotation-declared parameters
 *   plus the number of interpreter-supplied parameters.
 * </li>
 * </ul>
 */
@Target({ElementType.METHOD})
@Retention(RetentionPolicy.RUNTIME)
public @interface SkylarkCallable {

  /**
   * Name of the method, as exposed to Skylark.
   */
  String name() default "";

  /**
   * The documentation text in Skylark. It can contain HTML tags for special formatting.
   *
   * <p>It is allowed to be empty only if {@link #documented()} is false.
   */
  String doc() default "";

  /**
   * If true, the function will appear in the Skylark documentation. Set this to false if the
   * function is experimental or an overloading and doesn't need to be documented.
   */
  boolean documented() default true;

  /**
   * If true, this method will be considered as a field of the enclosing Java object. E.g., if set
   * to true on a method {@code foo}, then the callsites of this method will look like {@code
   * bar.foo} instead of {@code bar.foo()}. The annotated method must be parameterless and {@link
   * #parameters()} should be empty.
   */
  boolean structField() default false;

  /**
   * Number of parameters in the signature that are mandatory positional parameters. Any parameter
   * after {@link #mandatoryPositionals()} must be specified in {@link #parameters()}. A negative
   * value (default is {@code -1}), means that all arguments are mandatory positionals if {@link
   * #parameters()} remains empty. If {@link #parameters()} is non empty, then a negative value for
   * {@link #mandatoryPositionals()} is taken as 0.
   */
  int mandatoryPositionals() default -1;

  /**
   * List of parameters this function accept after the {@link #mandatoryPositionals()} parameters.
   */
  Param[] parameters() default {};

  /**
   * Set it to true if the Java method may return <code>null</code> (which will then be converted to
   * <code>None</code>). If not set and the Java method returns null, an error will be raised.
   */
  boolean allowReturnNones() default false;

  /**
   * If true, the location of the call site will be passed as an argument of the annotated function.
   * (Thus, the annotated method signature must contain Location as a parameter. See the
   * interface-level javadoc for details.)
   */
  boolean useLocation() default false;

  /**
   * If true, the AST of the call site will be passed as an argument of the annotated function.
   * (Thus, the annotated method signature must contain FuncallExpression as a parameter. See the
   * interface-level javadoc for details.)
   */
  boolean useAst() default false;

  /**
   * If true, the Skylark Environment will be passed as an argument of the annotated function.
   * (Thus, the annotated method signature must contain Environment as a parameter. See the
   * interface-level javadoc for details.)
   */
  boolean useEnvironment() default false;
}
