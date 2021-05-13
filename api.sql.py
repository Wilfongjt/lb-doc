from pprint import pprint
import os

##########
# Generate User
##########

# c is optinal but validate when present
# C is required
# r is optinal but validate when present
# R is required
# u is optinal but validate when present
# U is required

# pksk
# sktk
'''
Define API
1. create definitions
'''
'''
Expand API Definition
1. augment definitions
2. inject functPattern
3. expand Chelate
4. expand Criteria
 
'''
'''
Script API
1. Validate Token and Set Role
2. Verify Expected Token Role(s)
3. Validate Parameters
4. User Specific Data Assembly
5. Execute Function

INSERT

QUERY
Criteria for query by user
* query by api_user by username
* query by api_admin by username or guid

'''
'''
-- required
if not(criteria ? 'username') or not(criteria ? 'password') then
-- validation
if criteria ? 'username' then
if criteria ? 'password' then  
if criteria ? 'displayname' then

    
'''

'''____        __ _       _ _   _                 
 |  __ \      / _(_)     (_) | (_)                
 | |  | | ___| |_ _ _ __  _| |_ _  ___  _ __  ___ 
 | |  | |/ _ \  _| | '_ \| | __| |/ _ \| '_ \/ __|
 | |__| |  __/ | | | | | | | |_| | (_) | | | \__ \
 |_____/ \___|_| |_|_| |_|_|\__|_|\___/|_| |_|___/
                                                  
'''

#  "keys":'{"pk":"username","sk":"const#USER","tk":"*"}',

definitions = {
    "user_chelate": {
        "pk": "username",
        "sk": "const#USER",
        "tk": "guid",
        "form": {
            "username": {"type": "email", "input": "CruD", "output": "R"},
            "password": {"type": "password", "input": "Cu", "output": False},
            "displayname": {"type": "TEXT", "input": "cu", "output": "R"}
        },
        "active": {"default": True},
        "created": {"default": "NOW()"},
        "updated": {"default": "NOW()"},
        "owner": {"default": "current_setting('request.jwt.claim.key')"}
    },
    "user": {
        "name": "user",
        "schema": "api_0_0_1",
        "chelate": "user_chelate",
        "type": "const#USER",
        "roles": "roles",
        "runAsRole": "api_guest",
        "tokenRole": "api_user",
        "parameters": {"POST": {"token": "TEXT", "form": "JSON"},
                       "GET": {"token": "TEXT", "criteria": "JSON", "options": "JSON"},
                       "PUT": {"token": "TEXT", "pk": "TEXT", "form": "JSON"},
                       "DELETE": {"token": "TEXT", "pk": "TEXT"}},
        "roles": {"api_guest": {"privileges": "C", "token": "Gk"},
                  "api_user": {"privileges": "RUD", "token": "UK"},
                  "api_admin": {"privileges": "r", "token": "AK"}
                  },
        "passwordHashOn": "password"
    }
}
print('parameters',definitions['user']['parameters']['POST'])
#exit(0)
'''
           _____ _____ 
     /\   |  __ \_   _|
    /  \  | |__) || |  
   / /\ \ |  ___/ | |  
  / ____ \| |    _| |_ 
 /_/    \_\_|   |_____|

'''
#f = [fld for fld in d["form"]]
#print('f',f)
class API(dict):
    def __init__(self, _definitions):
        # transform
        methods = ["POST","GET","PUT","DELETE"]
        for key in _definitions:
            # Augment Definitions
            definition = _definitions[key].copy()

            if 'schema' in definition:
                print('chelate', definition['chelate'])
                chelate = _definitions[definition['chelate']]
                definition['chelate'] = chelate
                definition['funcPattern']={}
                for method in methods:
                    print('method', method)
                    self[key]=definition
                    # functPattern
                    name = definition['name']
                    # ""
                    # parameters = ['{} {}'.format(param,definition['parameters'][method][param]) for param in definition['parameters'][method]]
                    parameters = ['{}'.format(definition['parameters'][method][param]) for param in definition['parameters'][method]]
                    params = ', '.join(parameters)
                    print('params ', params)

                    definition['funcPattern'][method] = '{}({})'.format(name, params)
                    #definition['funcPattern'][method]= 'xxx'#'{}({})'.format(name, params)


#apiDefinitions = API(definitions)

#pprint(apiDefinitions)
#exit(0)

class FunctionTemplate(list):
    def __init__(self, method, apiDefinition):
        # convert to Postgres API Script
        # definition is a single function definition
        self.method = method
        self.definition = apiDefinition
        #self.parameterList = ['{} {}'.format(param,self.definition['parameters'][param]) for param in self.definition['parameters']]
        self.parameterList = None
        self.privileges=None
        self.tokenClaims=None
        # formatting
        #self.warning()
        self.nameFunction()
        self.declareVariables()
        self.begin()
        self.switchToRole(self.definition['runAsRole'])
        self.validateParameters()
        #self.startDataAssembly()
        #self.assembleDataHashPassword()
        self.assembleData()
        self.function()
        self.end()
        self.grantFunction()

    def getParameterList(self):
        if not self.parameterList:
            # ["<value> <type>","<value> <type>",...]
            #print('self.definition[parameters]',self.definition['parameters'])
            self.parameterList = ['{} {}'.format(param, self.definition['parameters'][self.method][param]) for param in
                                  self.definition['parameters'][self.method]]
        return self.parameterList

    def getTokenByRole(self):
        if not self.tokenClaims:
            self.tokenClaims = {r: self.definition['roles'][r]['token'] for r in self.definition['roles']}
        return self.tokenClaims

    def getPrivilegesByRole(self):
        if not self.privileges:
            self.privileges = {r: self.definition['roles'][r]['privileges'] for r in self.definition['roles']}
        return self.privileges

    def getKeys(self):
        #keys = self.definition['keys']
        c = self.definition['chelate']
        rc = '{"pk":"%p","sk":"%s","tk":"%t"}'
        if '#' not in c['pk']:
            rc = rc.replace('%p',c['pk'])
        else:
            rc = rc.replace('%p','TBD')

        if 'const#' in c['sk']:
            rc = rc.replace('%s',c['sk'])
        else:
            rc = rc.replace('%s','TBD')

        if 'guid' in c['tk']:
            rc = rc.replace('%t','*')
        else:
            rc = rc.replace('%t','TBD')
        return rc

    #def warning(self):
    #    filename = __file__.split('/')
    #    filename = filename[len(filename)-1]
    #    rc = '''
    #    -- This function was generated using {}
    #    '''.format(filename)
    #    #self.append(rc)
    #    return rc

    def nameFunction(self):
        #pprint(self.definition)
        schema=self.definition['schema']
        # parameters = ['{} {}'.format(param,self.definition['parameters'][param]) for param in self.definition['parameters']]
        name = self.definition['name']
        name = '{}({})'.format(name, ','.join(self.getParameterList()))
        result = '''CREATE OR REPLACE FUNCTION {}.{}  RETURNS JSONB AS $$'''.format( schema, name)
        self.append(result)
        return self

    def declareVariables(self):
        rc = ''
        if 'POST' in self.method:
            rc = '''    Declare _form JSONB; Declare result JSONB; Declare _chelate JSONB := '{}'::JSONB;Declare tmp TEXT;'''
        if 'GET' in self.method:
            rc = '''    Declare _criteria JSONB; Declare result JSONB;'''
        if 'PUT' in self.method:
            rc = '''    Declare _chelate JSONB := '{}'::JSONB; Declare _criteria JSONB := '{}'::JSONB; _form JSONB := '{}'::JSONB; Declare result JSONB;'''
        if 'DELETE' in self.method:
            rc = '''    Declare result JSONB; Declare _criteria JSONB := '{}'::JSONB;'''

        self.append(rc)

        return self

    def begin(self):
        #titleComment = '-- [Function: {} {} given {}]'.format( self.definition['name'].title(), self.method, ','.join(self.parameterList))
        titleComment = '-- [Function: {} {}]'.format( self.definition['name'].title(), self.method)

        methodComment = ''


        if self.method == 'DELETE':
            methodComment = '''
            -- [Description: Remove a {} from the table]
            -- [Parameters: {}]
            -- [Delete by primary key]
            -- [pk is <text-value> or guid#<value>'''\
                .format(self.definition['name'],','.join(self.parameterList))
        elif self.method == 'PUT':
            methodComment = '''
            -- [Description: Change the values of a {} chelate]
            -- [Parameters: {}]
            -- [Update by primary key]
            -- [pk is <text-value> or guid#<value>'''\
                .format(self.definition['name'],','.join(self.parameterList))
        elif self.method == 'POST':
            methodComment = '''
            -- [Description: Store the original values of a {} chelate]
            -- [Parameters: {}]
            -- [pk is <text-value> or guid#<value>'''\
                .format(self.definition['name'],','.join(self.parameterList))
        elif self.method == 'GET':
            methodComment = '''
            -- [Description: Find the values of a {} chelate]
            -- [Parameters: {}]'''\
                .format(self.definition['name'],','.join(self.parameterList))

        rc = '''
        BEGIN
          {}
          {}'''.format(titleComment,methodComment)

        self.append(rc)
        return self

    def switchToRole(self, role):

        rc = '''
          -- [Switch to {} Role]
          set role {}; '''.format(role, role)
        self.append(rc)
        return self

    def validateParameters(self):
        #for param in self.definition['parameters']:

        for param in self.definition['parameters'][self.method]:
            if param == 'token':
                self.validateToken()
            elif param == 'form':
                self.validateForm()
            elif param == 'options':
                self.validateOptions()
            elif param == 'criteria':
                self.validateCriteria()
            elif param == 'pk':
                self.validatePk()
            else:
                print('uk param', param)

        return self

    def validatePk(self):

        rc = '''
          -- [Validate pk parameter]
          if pk is NULL then
              RESET ROLE;
              -- [Fail 400 when pk is NULL]
              return '{"status":"400","msg":"Bad Request"}'::JSONB;
          end if;'''
        self.append(rc)

    def validateToken(self):
        tokenRole = self.definition['tokenRole']
        rc = '''
          -- [Validate token parameter]
          result := base_0_0_1.validate_token(token) ;
          if result is NULL then
            -- [Fail 403 When token is invalid]
            RESET ROLE;
            return format({},CURRENT_USER)::JSONB;
          end if;'''.format('\'{"status":"403","msg":"Forbidden","extra":"Invalid token","user":"%s"}\'')

        self.append(rc)
        scopeVerificationList = []
        keyVerificationList =[]
        if self.method == 'POST':
            scopeVerificationList = ['not(result ->> \'scope\' = \'{}\')'.format(role) for role in
                                     self.getPrivilegesByRole() if 'C' in self.getPrivilegesByRole()[role].upper() ]
            #keyVerificationList = ['not(result ->> \'key\' = \'{}\')'.format('0') for role in
            #                       self.getTokenByRole() if 'C' in self.getPrivilegesByRole()[role].upper()
            #                                                 and 'K' in self.getTokenByRole()[role]]
        elif self.method == 'GET':
            scopeVerificationList = ['not(result ->> \'scope\' = \'{}\')'.format(role) for role in
                                     self.getPrivilegesByRole() if 'R' in self.getPrivilegesByRole()[role].upper()]
            #keyVerificationList = ['not(result ->> \'key\' = \'{}\')'.format('0') for role in
            #                       self.getTokenByRole() if 'R' in self.getPrivilegesByRole()[role].upper()
            #                                                 and 'K' in self.getTokenByRole()[role]]
        elif self.method == 'PUT':
            scopeVerificationList = ['not(result ->> \'scope\' = \'{}\')'.format(role) for role in
                                     self.getPrivilegesByRole() if 'U' in self.getPrivilegesByRole()[role].upper()]
            #keyVerificationList = ['not(result ->> \'key\' = \'{}\')'.format('0') for role in
            #                         self.getTokenByRole() if 'U' in self.getPrivilegesByRole()[role].upper()
            #                                                  and 'K' in self.getTokenByRole()[role]]

        elif self.method == 'DELETE':
            scopeVerificationList = ['not(result ->> \'scope\' = \'{}\')'.format(role) for role in
                                     self.getPrivilegesByRole() if 'D' in self.getPrivilegesByRole()[role].upper()]
            #keyVerificationList = ['not(result ->> \'key\' = \'{}\')'.format('0') for role in
            #                       self.getTokenByRole() if 'D' in self.getPrivilegesByRole()[role].upper()
            #                                                 and 'K' in self.getTokenByRole()[role]]
        rc = '''
          -- [Verify token has expected scope]
          if {} then
              RESET ROLE;
              -- [Fail 401 when unexpected scope is detected]
              return '{}'::JSONB;
          end if; '''.format(' and '.join(scopeVerificationList), '{"status":"401","msg":"Unauthorized"}')

        self.append(rc)

        if len(keyVerificationList):
            rc = '''
             -- [Verify token has expected key]
             if {} then
                  RESET ROLE;
                  -- [Fail 401 when unexpected key is detected]
                  return '{}'::JSONB;
             end if;'''.format(' and '.join(keyVerificationList), '{"status":"401","msg":"Unauthorized"}')
            self.append(rc)

        return self


    def validateForm(self):
        #method=self.definition['method']
        perm = 'C'

        if self.method == 'PUT':
            perm = 'U'
        form=self.definition['chelate']['form']
        required = ['not(_form ? \'{}\')'.format(nm) for nm in form if perm in form[nm]['input']]
        # optional = ['_form ? \'{}\' and not(\'{}\')'.format(nm, nm) for nm in form if 'c' in form[nm]['input']]

        rc = '''
        
           
          -- [Validate form parameter] 
          if form is NULL then
              -- [Fail 400 when form is NULL]
              RESET ROLE;
              return '{"status":"400","msg":"Bad Request"}'::JSONB;
          end if;    
          
          _form := form::JSONB; 
        '''

        if len(required) > 0:
            rc += '''
          -- [Validate Requred form fields]
          if {} then  
              -- [Fail 400 when form is missing requrired field]
              RESET ROLE;
              return {}::JSONB;
          end if;'''\
            .format(
                   ' or '.join(required),
                   '\'{"status":"400","msg":"Bad Request"}\''
                   )
        else:
            rc += '''
          -- [Validate Requred form fields]
          -- [No required {} form fields ]
            '''.format(self.method)
            rc += '''
          -- [Validate optional form fields]
          -- [No optional {} form fields]
            '''.format(self.method)
        self.append(rc)
        return self
    def hashPassword(self):
        rc = '''
        -- [Hash password when found]
        if _form ? 'password' then
            _form := _form || format('{"password": "%s"}',crypt(form ->> 'password', gen_salt('bf')) )::JSONB; 
        end if;  
        '''
        self.append(rc)

    #def hashPassword(self):
    #    if self.method == 'POST' or self.method == 'PUT':
    #        rc = '''
    #    -- [Hash Password x]
    #    if (_chelate ->> 'form')::JSONB ? '%k' then
    #            _form := (_chelate ->> 'form')::JSONB;
    #            _form := _form || format('{"password": "%s"}',crypt(form ->> '%k', gen_salt('bf')) )::JSONB;
    #            _chelate := _chelate || format('{"form": %s}',_form)::JSONB;
    #    end if;'''
    #        self.append(rc)

    def validateOptions(self):
        rc = '''
          -- Validate Options'''
        self.append(rc)
        return self

    def validateCriteria(self):
        rc = '''
          -- Validate Criteria'''
        self.append(rc)

    def startDataAssembly(self):
        rc = '''
          -- [Data Assembly]'''
        self.append(rc)
        return self

    def assembleDataHashPassword(self):
        rc = '''
          -- Hash Password is Off'''
        if self.method == 'POST' or self.method == 'PUT':
            rc = '''
              -- [Hash Password is On]'''
            self.append(rc)

        self.append(rc)
        return self

    def assembleData(self):
        rc = '''
          -- [Assemble Data]'''
        self.append(rc)
        return self

    def function(self):
        method=self.definition['method']
        name= self.definition['name']

        rc = '''
          -- [API {} {} Function]
          TBD
          '''.format(method, name)

        self.append(rc)
        return self

    def end(self):
        rc = '''
          RESET ROLE;
          -- [Return {status,msg,insertion}]
          return result;    
        END;
        $$ LANGUAGE plpgsql;'''
        self.append(rc)
        return self


    def grantFunction(self):
        #method=self.definition['runAsRole']
        schema=self.definition['schema']
        #name=self.definition['name']
        runAsRole=self.definition['runAsRole']
        rc = 'grant EXECUTE on FUNCTION {}.{} to {};' \
            .format(schema, self.definition['funcPattern'][self.method], runAsRole)
        self.append(rc)
        return self


    def toString(self):
        return '\n'.join(self)
'''
  _____          _   
 |  __ \        | |  
 | |__) |__  ___| |_ 
 |  ___/ _ \/ __| __|
 | |  | (_) \__ \ |_ 
 |_|   \___/|___/\__|
                     
                     

'''
class PostTemplate(FunctionTemplate):
    def __init__(self,definition):
        super().__init__('POST',definition)

    '''
    def getKeys(self):
        #keys = self.definition['keys']
        c = self.definition['chelate']
        rc = '{"pk":"%p","sk":"%s","tk":"%t"}'
        if '#' not in c['pk']:
            rc = rc.replace('%p',c['pk'])
        else:
            rc = rc.replace('%p','TBD')

        if 'const#' in c['sk']:
            rc = rc.replace('%s',c['sk'])
        else:
            rc = rc.replace('%s','TBD')

        if 'guid' in c['tk']:
            rc = rc.replace('%t','*')
        else:
            rc = rc.replace('%t','TBD')

        return rc
    '''
    def getInsert(self, role, privileges):
        rc = '''             
              -- [Chelate Data]
              _chelate := base_0_0_1.chelate(\'{}\'::JSONB, _form); -- chelate with keys on insert
              -- [Stash guid for insert]
              tmp = set_config('request.jwt.claim.key', replace(_chelate ->> 'tk','guid#',''), true); 
              -- If is_local is true, the new value will only apply for the current transaction.
              --raise notice 'tmp %', tmp;'''\
            .format(self.getKeys())
        return rc

    def assembleData(self):
        rc = '''
        -- [Assemble Data]'''
        self.append(rc)

        self.hashPassword()

        rc = '          '
        #print('getPrivilegesByRole', self.getPrivilegesByRole())
        self.append('        -- user specific stuff')
        lst = ['if CURRENT_USER = \'{}\' then\n {} \n'
                  .format(role, self.getInsert(role, self.getPrivilegesByRole()[role]))
                  for role in self.getPrivilegesByRole()
                      if 'C' in self.getPrivilegesByRole()[role].upper()]

        rc += '           els'.join(lst)
        rc += '\n          end if;'
        self.append(rc)
        return self

    def function(self):
        #method = self.definition['method']
        name = self.definition['name']

        rc = '''
    
          -- [Insert {} Chelate]
          result := base_0_0_1.insert(_chelate);'''.format(name)
        self.append(rc)
        return self
'''
   _____      _   
  / ____|    | |  
 | |  __  ___| |_ 
 | | |_ |/ _ \ __|
 | |__| |  __/ |_ 
  \_____|\___|\__|
                  
'''



class GetTemplate(FunctionTemplate):
    def __init__(self,definition):
        super().__init__('GET',definition)


    def getKey(self, value):
        # all upper are constants made up of const#value eg const#USER
        # lowercase are field names
        if '#' in value:
            return value.split('#')[0]
        return value

    def getValue(self, value):
        s = value.split('#')
        if s[0] == 'guid':
            return s[1]
        elif s[0] == 'const':
            return '\'{}\''.format(s[1])
        return 'criteria ->> {}'.format(value)

    def getQuery(self):
        rc = '''
             
              if _criteria ? 'pk' and _criteria ? 'sk' then
                  -- [Primary query {pk,sk}]
                  _criteria = format('{"pk":"%s", "sk":"%s"}',_criteria ->> 'pk',_criteria ->> 'sk')::JSONB;
              elsif _criteria ? 'pk' and not(_criteria ? 'sk') then
                   -- [Primary query {pk,sk:*}]
                  _criteria = format('{"pk":"%s", "sk":"%s"}',_criteria ->> 'pk','*')::JSONB;
              elsif _criteria ? 'sk' and _criteria ? 'tk' then
                  -- [Secondary query {sk,tk}]
                  _criteria = format('{"sk":"%s", "tk":"%s"}',_criteria ->> 'sk',_criteria ->> 'tk')::JSONB;
              elsif _criteria ? 'sk' and not(_criteria ? 'tk') then
                  -- [Secondary query {sk,tk:*}]
                  _criteria = format('{"sk":"%s", "tk":"%s"}',_criteria ->> 'sk','*')::JSONB;
              elsif _criteria ? 'xk' and _criteria ? 'yk' then
                  -- [Teriary query {tk,sk} aka {xk, yk}]
                  _criteria = format('{"xk":"%s", "yk":"%s"}',_criteria ->> 'xk',_criteria ->> 'yk')::JSONB;
              elsif _criteria ? 'xk' and not(_criteria ? 'yk') then
                  -- [Teriary query {tk} aka {xk}]
                  _criteria = format('{"xk":"%s", "yk":"%s"}',_criteria ->> 'xk','*')::JSONB;
              elsif _criteria ? 'yk' and _criteria ? 'zk' then
                  -- [Quaternary query {sk,pk} akd {yk,zk}
                  _criteria = format('{"yk":"%s", "zk":"%s"}',_criteria ->> 'yk',_criteria ->> 'zk')::JSONB;
              elsif _criteria ? 'yk' and not(_criteria ? 'zk') then
                  -- [Quaternary query {yk}
                  _criteria = format('{"yk":"%s", "zk":"%s"}',_criteria ->> 'yk','*')::JSONB;                
              end if;
        '''

        return rc

    def assembleData(self):
        self.append('          -- [Assemble user specific data]')
        rc = '          _criteria=criteria::JSONB;\n'
        rc += '          '
        #         lst = ['if CURRENT_USER = \'{}\' then\n {} \n'.format(role,self.getQuery()) for role in self.getPrivilegesByRole() if self.definition['method']=='GET' and 'R' in self.getPrivilegesByRole()[role].upper() ]
        lst = ['if CURRENT_USER = \'{}\' then\n {} \n'.format(role,self.getQuery()) for role in self.getPrivilegesByRole() if 'R' in self.getPrivilegesByRole()[role].upper() ]
        rc += '           els'.join(lst)
        rc += '\n          end if;'
        self.append(rc)
        return self

    def function(self):
        #method = self.definition['method']
        name = self.definition['name']
        rc = '''
          -- [API {} {} Function]
          result := base_0_0_1.query(_criteria);'''.format(self.method, name)
        self.append(rc)
        return self



'''
  _____       _      _       
 |  __ \     | |    | |      
 | |  | | ___| | ___| |_ ___ 
 | |  | |/ _ \ |/ _ \ __/ _ \
 | |__| |  __/ |  __/ ||  __/
 |_____/ \___|_|\___|\__\___|
                             
'''

class DeleteTemplate(FunctionTemplate):
    def __init__(self,definition):
        super().__init__('DELETE',definition)



    def getDelete(self):

        d = self.definition

        rc = '''
              if strpos(pk,'#') > 0 then
                -- [Assume <key> is valid when # is found ... at worst, delete will end with a 404]
                -- [Delete by pk:<key>#<value> and sk:{} when undefined prefix]                
                _criteria := format('{}',pk)::JSONB;'''\
        .format(
            d['type'],
            '{"pk":"%s", "sk":"%k"}'.replace('%k', d['type']),
        )
        rc += '''
              else
                -- [Wrap pk as primary key when # is not found in pk]
                -- [Delete by pk:{}#<value> and sk:{} when <key># is not present]
                _criteria := format('{}',pk)::JSONB;              
              end if;
        '''.format(
                  d['chelate']['pk'],
                  d['type'],
                  '{"pk":"%k#%s", "sk":"%c"}'.replace('%k', d['chelate']['pk']).replace('%c', d['type'])
        )

        return rc

    def assembleData(self): #Delete
        self.append('          -- [Assemble user specific data]')
        #rc = '          _criteria=criteria::JSONB;\n'
        rc = '          '
        #         lst = ['if CURRENT_USER = \'{}\' then\n {} \n'.format(role,self.getDelete(role,self.definition['privileges'][role])) for role in self.definition['privileges'] if self.definition['method']=='DELETE' and self.definition['privileges'][role] ]
        lst = ['if CURRENT_USER = \'{}\' then\n {} \n'.format(role,self.getDelete())
               for role in self.getPrivilegesByRole()
               if 'D' in self.getPrivilegesByRole()[role].upper() ]
        rc += '           els'.join(lst)
        rc += '\n          end if;'
        self.append(rc)
        return self

    def function(self):
        #method = self.definition['method']
        name = self.definition['name']
        rc = '''
          -- [API {} {} Function]
          result := base_0_0_1.delete(_criteria);'''.format(self.method, name)
        self.append(rc)
        return self

'''
  _    _           _       _       
 | |  | |         | |     | |      
 | |  | |_ __   __| | __ _| |_ ___ 
 | |  | | '_ \ / _` |/ _` | __/ _ \
 | |__| | |_) | (_| | (_| | ||  __/
  \____/| .__/ \__,_|\__,_|\__\___|
        | |                        
        |_|                        

'''
class PutTemplate(FunctionTemplate):
    def __init__(self,definition):
        super().__init__('PUT',definition)


    def getUpdate(self, role, privileges):
        d = self.definition

        rc = '''
              if strpos(pk,'#') > 0 then
                -- [Assume <key> is valid when # is found ... at worst, delete will end with a 404]
                -- [Delete by pk:<key>#<value> and sk:{} when undefined prefix]      
                          
                _criteria := format('{}',pk)::JSONB;''' \
            .format(
            d['type'],
            '{"pk":"%s", "sk":"%k"}'.replace('%k', d['type']),
        )
        rc += '''
              else
                -- [Wrap pk as primary key when # is not found in pk]
                -- [Delete by pk:{}#<value> and sk:{} when <key># is not present]
                _criteria := format('{}',pk)::JSONB;              
              end if;
        '''.format(
            d['chelate']['pk'],
            d['type'],
            '{"pk":"%k#%s", "sk":"%c"}'.replace('%k', d['chelate']['pk']).replace('%c', d['type'])
        )
        rc += '''
              -- merget pk and sk
              _chelate := _chelate || _criteria;
              -- add the provided form
              _chelate := _chelate || format('{"form": %s}',_form)::JSONB; '''
        return rc
    def assebleDataByUser(self):
        self.append(' ')
        self.append('        -- [Assemble user specific data]')
        # rc = '          _criteria=criteria::JSONB;\n'
        rc = '          '
        #         lst = ['if CURRENT_USER = \'{}\' then\n {} \n'.format(role,self.getDelete(role,self.definition['privileges'][role])) for role in self.definition['privileges'] if self.definition['method']=='DELETE' and self.definition['privileges'][role] ]
        # privileges = self.getPrivilegesByRole()
        lst = ['if CURRENT_USER = \'{}\' then\n {} \n'.format(role,
                                                              self.getUpdate(role, self.getPrivilegesByRole()[role]))
               for role in self.getPrivilegesByRole()
               if 'U' in self.getPrivilegesByRole()[role].upper()]
        rc += '           els'.join(lst)
        rc += '\n          end if;'
        self.append(rc)

    def assembleData(self):
        #rc = '''
        #_form := form::JSONB;
        #'''
        #self.append(rc)
        self.hashPassword()
        self.assebleDataByUser()

        return self

    def function(self):
        #method = self.definition['method']
        name = self.definition['name']
        #rc = ''''''
        if 'passwordHashOn' in self.definition and self.definition['passwordHashOn']:

            rc = '''
          -- [Hash password when found]
          if _form ? 'password' then
              --_form := (_chelate ->> 'form')::JSONB;
              _form := _form || format('{"password": "%s"}',crypt(form ->> 'password', gen_salt('bf')) )::JSONB;
          end if;
            '''
        rc = '''
          -- [API {} {} Function]
          result := base_0_0_1.update(_chelate);'''.format(self.method, name)
        self.append(rc)
        return self

'''
  _    _                 _ _           
 | |  | |               | | |          
 | |__| | __ _ _ __   __| | | ___ _ __ 
 |  __  |/ _` | '_ \ / _` | |/ _ \ '__|
 | |  | | (_| | | | | (_| | |  __/ |   
 |_|  |_|\__,_|_| |_|\__,_|_|\___|_|   
                                       
                                       
'''
def warning():
    filename = __file__.split('/')
    filename = filename[len(filename)-1]
    rc = '''
    -- This function was generated using {}
    '''.format(filename)
    #self.append(rc)
    return rc

apiDefinitions = API(definitions)

pprint(apiDefinitions)
#exit(0)

pageList = []
pageList.append('\c one_db')
pageList.append('SET search_path TO api_0_0_1, base_0_0_1, public;')
pageList.append(warning())
for func in apiDefinitions:
    pageList.append(PostTemplate(apiDefinitions[func]).toString())
    pageList.append(GetTemplate(apiDefinitions[func]).toString())
    pageList.append(DeleteTemplate(apiDefinitions[func]).toString())
    pageList.append(PutTemplate(apiDefinitions[func]).toString())

    #print('postgres script ')
    #if apiDefinitions[func]['method'] == 'POST':
    #    print(PostTemplate(apiDefinitions[func]).toString())
    #if apiDefinitions[func]['method'] == 'GET':
    #    print(GetTemplate(apiDefinitions[func]).toString())
    #if apiDefinitions[func]['method'] == 'DELETE':
    #    print(DeleteTemplate(apiDefinitions[func]).toString())
    #if apiDefinitions[func]['method'] == 'PUT':
    #    print(PutTemplate(apiDefinitions[func]).toString())

print('\n\n'.join(pageList))

cwd = os.getcwd()
outfolder = '../one_db/sql'
fn='{}/{}'.format(outfolder, '24.api.0.0.1.user.sql')
print('fn',fn)
with open(fn, 'w') as f:
    f.write('\n\n'.join(pageList))
# write to file



