## Define mini-templates for each portion of the doco.

<%!
  def indent(s, spaces=4):
      new = s.replace('\n', '\n' + ' ' * spaces)
      return ' ' * spaces + new.strip()
%>

<%def name="deflist(s)"> ${indent(s)[1:]}</%def>

<%def name="h1(s)"># ${s}
</%def>

<%def name="h2(s)">## ${s}
</%def>

<%def name="h3(s)">### ${s}
</%def>

<%def name="h4(s)">#### ${s}
</%def>

<%def name="function(func)" buffered="True">
    <%
        returns = show_type_annotations and func.return_annotation() or ''
        if returns:
            returns = ' \N{non-breaking hyphen}> ' + returns
    %>
${func.name}(${", ".join(func.params(annotate=show_type_annotations))})${returns}
${func.docstring | deflist}
</%def>

<%def name="variable(var)" buffered="True">
    <%
        annot = show_type_annotations and var.type_annotation() or ''
        if annot:
            annot = ': ' + annot
    %>
${var.name}${annot}
${var.docstring | deflist}
</%def>

<%def name="class_(cls)" buffered="True">
${h3(cls.name)}
    ${cls.name}(${", ".join(cls.params(annotate=show_type_annotations))})

${indent(cls.docstring)}

<%
  class_vars = cls.class_variables(show_inherited_members, sort=sort_identifiers)
  static_methods = cls.functions(show_inherited_members, sort=sort_identifiers)
  inst_vars = cls.instance_variables(show_inherited_members, sort=sort_identifiers)
  methods = cls.methods(show_inherited_members, sort=sort_identifiers)
  mro = cls.mro()
  subclasses = cls.subclasses()
%>
% if mro:
${h4('Ancestors (in MRO)')}
    % for c in mro:
    * ${c.refname}
    % endfor

% endif
% if subclasses:
${h4('Descendants')}
    % for c in subclasses:
    * ${c.refname}
    % endfor

% endif
% if class_vars:
${h4('Class variables')}
    % for v in class_vars:
${variable(v) | indent}

    % endfor
% endif
% if static_methods:
${h4('Static methods')}
    % for f in static_methods:
${function(f) | indent}

    % endfor
% endif
% if inst_vars:
${h4('Instance variables')}
    % for v in inst_vars:
${variable(v) | indent}

    % endfor
% endif
% if methods:
${h4('Methods')}
    % for m in methods:
${function(m) | indent}

    % endfor
% endif
</%def>

## Start the output logic for an entire module.

<%
  variables = module.variables(sort=sort_identifiers)
  classes = module.classes(sort=sort_identifiers)
  functions = module.functions(sort=sort_identifiers)
  submodules = module.submodules()
  heading = 'Namespace' if module.is_namespace else 'Module'
%>

${h1(heading + " " + module.name)}

${module.docstring}

% if submodules:
${h2("Sub-modules")}

    % for m in submodules:
* ${m.name}
    % endfor
% endif

% if variables:
${h2("Variables")}

    % for v in variables:
${variable(v)}

    % endfor
% endif

% if functions:
${h2("Functions")}

    % for f in functions:
${function(f)}

    % endfor
% endif

% if classes:
${h2("Classes")}

    % for c in classes:
${class_(c)}

    % endfor
% endif