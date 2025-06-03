load("@ytt:data", "data")

#! Return the component name, optional with a postfix.
def resourceName(v, postfix=""):
    name = v.name

    if postfix:
      name += "-" + postfix
    end

    return name
end

def resourceLabels(v):
  return {
    "app.kubernetes.io/version": v.version,
    "app.kubernetes.io/name": v.name,
    "app.kubernetes.io/managed-by": "ytt",
    "app.kubernetes.io/component": "microservice",
  }
end
